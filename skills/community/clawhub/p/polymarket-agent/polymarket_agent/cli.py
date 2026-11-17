"""`poly` CLI — human and agent interface.

AUDIT FIX (Medium — "Dangerous Code Execution", 97%): v1.0.2 handed a command
string to a shell in the `doctor` command, and shelled out to the `clawdbot`
binary with user values. Here no external process is spawned at all: dependency
checks use `importlib.util.find_spec` in-process, and config is local JSON.

AUDIT FIX (High — "Unvalidated Output Injection", 88%): all text coming from
outside (API, config, error messages) is printed with Rich markup DISABLED via
`safe()`, so that a `[/]` or `[link=...]` in a market title cannot forge output
in the user's terminal.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import time
from typing import List, Optional

import typer
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from . import __version__, alerts, guardrails, journal, keystore, markets, trading
from . import whales as whale_api
from .config import (
    KNOWN_KEYS,
    LOCKED_KEYS,
    ConfigError,
    Settings,
    load_settings,
    save_settings,
    set_value,
)
from .http import ApiError
from .paths import app_dir, halt_path

app = typer.Typer(
    name="poly",
    help="Polymarket Agent — prediction-market research with risk guard-rails.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)


def safe(value: object) -> str:
    """Neutralize Rich markup in untrusted content."""
    return escape(str(value))


def fail(message: str, code: int = 1) -> "typer.Exit":
    err_console.print(f"[red]✘[/red] {safe(message)}")
    return typer.Exit(code)


# ══════════════════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════════════════


@app.command(rich_help_panel="Setup")
def setup(
    force: bool = typer.Option(False, "--force", help="Overwrite the existing keystore."),
) -> None:
    """Create the ENCRYPTED wallet keystore (interactive wizard).

    The private key is read hidden, encrypted with scrypt+AES and written with
    0600 permissions. It never appears in argv, in an exported environment
    variable, in a log, or on screen.
    """
    console.print(
        Panel(
            "[bold]Polymarket wallet setup[/bold]\n\n"
            "[yellow]⚠ REAL MONEY.[/yellow] This skill signs on-chain orders on\n"
            "Polygon. Losses are [bold]irreversible[/bold] and there is no chargeback.\n\n"
            "[bold]Use a dedicated wallet[/bold], holding only what you\n"
            "accept losing. Never use your main wallet.",
            title="⚠ Financial risk warning",
            border_style="yellow",
        )
    )

    if keystore.keystore_exists() and not force:
        addr = keystore.keystore_address() or "?"
        console.print(f"\n[yellow]A keystore for {safe(addr)} already exists.[/yellow]")
        console.print("Use [cyan]poly setup --force[/cyan] to replace it.")
        raise typer.Exit(0)

    if not sys.stdin.isatty():
        raise fail(
            "`poly setup` needs an interactive terminal — the private key "
            "is never accepted as an argument or via a pipe."
        )

    import getpass

    console.print("\n[bold]1/3 — Private key[/bold] (hidden input, does not echo)")
    try:
        raw_key = getpass.getpass("Private key (0x...): ")
    except (EOFError, KeyboardInterrupt):
        raise fail("cancelled.")

    try:
        normalized = keystore.normalize_private_key(raw_key)
        address = keystore.address_for(normalized)
    except keystore.KeystoreError as exc:
        raise fail(str(exc))

    console.print(f"  [green]✔[/green] Wallet recognized: {safe(address)}")

    console.print("\n[bold]2/3 — Keystore passphrase[/bold] (protects the key at rest)")
    try:
        passphrase = getpass.getpass("Passphrase (min. 8 characters): ")
        confirm = getpass.getpass("Repeat the passphrase: ")
    except (EOFError, KeyboardInterrupt):
        raise fail("cancelled.")

    if passphrase != confirm:
        raise fail("the passphrases do not match.")

    try:
        keystore.save_key(normalized, passphrase)
    except keystore.KeystoreError as exc:
        raise fail(str(exc))

    del normalized, raw_key, passphrase, confirm

    console.print(f"  [green]✔[/green] Encrypted keystore at {safe(keystore.keystore_path())} (0600)")

    console.print("\n[bold]3/3 — Wallet type[/bold]")
    console.print(
        "  [dim]0 = EOA — the key owns the USDC (imported from MetaMask etc.)\n"
        "  1 = Polymarket email/magic proxy\n"
        "  2 = Polymarket wallet proxy (browser login)[/dim]"
    )
    console.print(
        "  If you deposited through the Polymarket site, it's almost certainly [cyan]1[/cyan] or [cyan]2[/cyan],\n"
        "  and you need to provide the address holding the balance:\n"
        "    [cyan]poly config --key signature_type --value 2[/cyan]\n"
        "    [cyan]poly config --key funder_address --value 0x...[/cyan]"
    )

    settings = load_settings()
    save_settings(settings)

    console.print(
        Panel(
            "[green]✅ Setup complete.[/green]\n\n"
            f"[bold]DRY-RUN[/bold] mode is [bold green]ON[/bold green]: orders are validated and\n"
            "journaled, but [bold]nothing is sent[/bold] to the exchange.\n\n"
            "Test everything first. To go live:\n"
            "  [cyan]poly config --key dry_run --value false[/cyan]\n\n"
            f"Current limits: ${settings.max_position_usd:.0f}/order, "
            f"${settings.max_daily_spend_usd:.0f}/day, {settings.max_bankroll_pct:.0f}% of bankroll.",
            border_style="green",
        )
    )


@app.command(rich_help_panel="Setup")
def config(
    key: Optional[str] = typer.Option(None, "--key", "-k", help="Config key to read/write."),
    value: Optional[str] = typer.Option(None, "--value", "-v", help="New value."),
    list_all: bool = typer.Option(False, "--list", "-l", help="Show the whole config."),
) -> None:
    """Read or write local config (JSON in ~/.openclaw/polymarket-agent).

    Only known keys are accepted, with type and range validated. Secrets
    cannot be written here — the private key only ever enters via `poly setup`.
    """
    settings = load_settings()

    if list_all or (not key and not value):
        table = Table(title="Configuration", show_lines=False)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        for name in sorted(KNOWN_KEYS):
            current = getattr(settings, name)
            style = ""
            if name == "dry_run":
                style = "green" if current else "yellow"
            if name == "autonomous_mode":
                style = "red" if current else "green"
            rendered = f"[{style}]{safe(current)}[/{style}]" if style else safe(current)
            # Locked fields are shown (the user needs to see the autonomy
            # state) but only `poly auto` can write them.
            table.add_row(
                name + (" [dim](poly auto)[/dim]" if name in LOCKED_KEYS else ""),
                rendered,
            )
        console.print(table)
        console.print(f"[dim]File: {safe(app_dir())}[/dim]")
        return

    if key and key not in KNOWN_KEYS:
        raise fail(f"unknown key: {key}. Use `poly config --list`.")

    if key and value is not None:
        try:
            stored = set_value(key, value)
        except ConfigError as exc:
            raise fail(str(exc))
        console.print(f"[green]✔[/green] {safe(key)} = {safe(stored)}")
        if key == "dry_run" and stored is False:
            console.print(
                "[bold yellow]⚠ DRY-RUN OFF — the next orders are REAL "
                "and irreversible.[/bold yellow]"
            )
        return

    if key:
        console.print(f"[cyan]{safe(key)}[/cyan] = {safe(getattr(settings, key))}")


@app.command(rich_help_panel="Setup")
def doctor() -> None:
    """Diagnostic for the install and the active risk limits.

    Only checks THIS skill's dependencies, inside the process itself — does
    not inspect the host or run external commands.
    """
    console.print(Panel("Diagnostic — Polymarket Agent", border_style="cyan"))

    console.print("\n[bold]Dependencies[/bold]")
    ok = True
    for module, label in [
        ("py_clob_client", "py-clob-client (order signing)"),
        ("eth_account", "eth-account (encrypted keystore)"),
        ("requests", "requests (HTTP)"),
        ("rich", "rich (output)"),
        ("typer", "typer (CLI)"),
    ]:
        found = importlib.util.find_spec(module) is not None
        ok &= found
        mark = "[green]✔[/green]" if found else "[red]✘[/red]"
        console.print(f"  {mark} {label}")

    console.print(f"\n[bold]Python[/bold]\n  {sys.version.split()[0]} — {safe(sys.executable)}")

    console.print("\n[bold]Credentials[/bold]")
    if keystore.keystore_exists():
        addr = keystore.keystore_address() or "?"
        console.print(f"  [green]✔[/green] Encrypted keystore — wallet {safe(addr)}")
        from .paths import check_permissions, keystore_path

        warning = check_permissions(keystore_path())
        if warning:
            console.print(f"  [red]✘ {safe(warning)}[/red]")
    elif keystore.LEGACY_KEY_ENV in os.environ:
        gated = os.environ.get(keystore.LEGACY_ALLOW_ENV, "").strip().lower() in {
            "1", "true", "yes", "on",
        }
        if gated:
            console.print(
                f"  [yellow]⚠[/yellow] {keystore.LEGACY_KEY_ENV} + {keystore.LEGACY_ALLOW_ENV} set "
                "(legacy mode — visible to child processes; prefer `poly setup`)"
            )
        else:
            console.print(
                f"  [yellow]⚠[/yellow] {keystore.LEGACY_KEY_ENV} is set but {keystore.LEGACY_ALLOW_ENV} "
                "is not — the legacy path will refuse to activate (this is intentional)"
            )
    else:
        console.print("  [yellow]⚠[/yellow] No credential — run `poly setup`")

    settings = load_settings()
    console.print("\n[bold]Guard-rails[/bold]")
    dry = "[green]ON (nothing is sent)[/green]" if settings.dry_run else "[yellow]OFF — real orders[/yellow]"
    console.print(f"  Dry-run: {dry}")
    if guardrails.halt_active():
        console.print(f"  [red]■ KILL SWITCH ACTIVE[/red] — {safe(halt_path())}")
    auto = guardrails.autonomous_active(settings)
    if auto:
        left = (settings.autonomous_expires_at - time.time()) / 60
        console.print(f"  [red]Autonomous mode ACTIVE[/red] (expires in {left:.0f} min)")
    else:
        console.print("  Autonomous mode: [green]off[/green] (every order asks for confirmation)")
    console.print(f"  Per-order cap: ${settings.max_position_usd:.2f}")
    console.print(f"  Daily cap: ${settings.max_daily_spend_usd:.2f}")
    console.print(f"  Spend in the last 24h: ${journal.spend_since(86400):.2f}")

    if not ok:
        console.print("\n[yellow]Install what's missing with `./install.sh`.[/yellow]")


# ══════════════════════════════════════════════════════════════════════════════
# MARKETS (read-only)
# ══════════════════════════════════════════════════════════════════════════════


def markets_cmd(
    query: str = typer.Argument("", help="Search text. Empty = most traded."),
    limit: int = typer.Option(10, "--limit", "-l", min=1, max=100),
    min_volume: float = typer.Option(0.0, "--min-volume", help="Filter by 24h volume."),
    tokens: bool = typer.Option(False, "--tokens", help="Show each outcome's token_id."),
) -> None:
    """List active markets (public read, no credential)."""
    try:
        found = markets.search_markets(query or None, limit, min_volume)
    except markets.MarketError as exc:
        raise fail(str(exc))

    if not found:
        console.print("[yellow]No markets found.[/yellow]")
        return

    table = Table(title=f"Markets{f' — “{safe(query)}”' if query else ' trending'}")
    table.add_column("#", style="dim", width=3)
    table.add_column("Question", style="cyan", max_width=52, overflow="fold")
    table.add_column("Prices", style="green")
    table.add_column("24h volume", style="magenta", justify="right")

    settings = load_settings()
    for idx, market in enumerate(found, 1):
        illiquid = market.volume_24h < settings.min_volume_usd
        vol = f"${market.volume_24h:,.0f}"
        if illiquid:
            vol = f"[yellow]{vol} ⚠[/yellow]"
        table.add_row(str(idx), safe(market.question), safe(market.prices_label()), vol)

    console.print(table)
    console.print(
        f"[dim]⚠ = volume below ${settings.min_volume_usd:,.0f} "
        "(hard to get in/out without moving the price).[/dim]"
    )

    if tokens:
        for idx, market in enumerate(found, 1):
            console.print(f"\n[bold]{idx}. {safe(market.question)}[/bold]")
            if market.url:
                console.print(f"   [dim]{safe(market.url)}[/dim]")
            for out in market.outcomes:
                price = f"${out.price:.3f}" if out.price is not None else "?"
                console.print(
                    f"   • {safe(out.name):<12} {price:>8}  token_id={safe(out.token_id or '—')}"
                )


@app.command(rich_help_panel="Markets")
def market(
    market_id: str = typer.Argument(..., help="Numeric ID or market slug."),
) -> None:
    """Detail a market, including the token_ids needed to trade."""
    try:
        found = markets.get_market(market_id)
    except markets.MarketError as exc:
        raise fail(str(exc))
    if not found:
        raise fail(f"market not found: {market_id}")

    console.print(Panel(safe(found.question), border_style="cyan"))
    if found.url:
        console.print(f"[dim]{safe(found.url)}[/dim]")
    console.print(f"24h volume: ${found.volume_24h:,.0f}   Liquidity: ${found.liquidity:,.0f}")
    if found.end_date:
        console.print(f"Resolution: {safe(found.end_date)}")

    table = Table(title="Outcomes")
    table.add_column("Outcome", style="cyan")
    table.add_column("Price", style="green", justify="right")
    table.add_column("Implied prob.", justify="right")
    table.add_column("token_id", style="dim", overflow="fold")
    for out in found.outcomes:
        table.add_row(
            safe(out.name),
            f"${out.price:.3f}" if out.price is not None else "?",
            f"{out.implied_pct:.1f}%" if out.implied_pct is not None else "?",
            safe(out.token_id or "—"),
        )
    console.print(table)


# ══════════════════════════════════════════════════════════════════════════════
# WHALE FLOW / SMART MONEY (public read)
# ══════════════════════════════════════════════════════════════════════════════


def _fmt_age(timestamp: int) -> str:
    if not timestamp:
        return "?"
    delta = max(0, int(time.time()) - timestamp)
    if delta < 60:
        return f"{delta}s"
    if delta < 3600:
        return f"{delta // 60}min"
    if delta < 86400:
        return f"{delta // 3600}h"
    return f"{delta // 86400}d"


@app.command(rich_help_panel="Flow & Smart Money")
def whales(
    min_usd: float = typer.Option(25_000, "--min", "-m", min=0,
                                  help="Minimum notional in USDC."),
    hours: float = typer.Option(1.0, "--hours", "-H", min=0.01, max=720,
                                help="Time window."),
    limit: int = typer.Option(20, "--limit", "-l", min=1, max=200),
    market: str = typer.Option("", "--market", help="Filter by conditionId."),
    side: str = typer.Option("", "--side", help="BUY or SELL."),
    alert: bool = typer.Option(
        False, "--alert",
        help="Alert mode: only unseen trades; prints NO_REPLY if there are none.",
    ),
    preview: bool = typer.Option(
        False, "--preview",
        help="With --alert, do not mark trades as already announced.",
    ),
) -> None:
    """🐋 Recent large trades — the whale tracker.

    The size filter is applied by Polymarket's server, so the query stays
    cheap even over long windows.
    """
    try:
        if alert:
            found = alerts.new_whales(
                min_notional=min_usd,
                window_seconds=int(hours * 3600),
                limit=limit,
                persist=not preview,
            )
            # Plain-text output: OpenClaw's cron suppresses delivery when the
            # output is exactly NO_REPLY.
            print(alerts.format_alert(found, min_usd))
            return

        found = whale_api.recent_whales(
            min_notional=min_usd,
            window_seconds=int(hours * 3600),
            limit=limit,
            market=market or None,
            side=side or None,
        )
    except ApiError as exc:
        raise fail(str(exc))

    if not found:
        console.print(
            f"[yellow]No trades above ${min_usd:,.0f} in the last "
            f"{hours:g}h.[/yellow]"
        )
        return

    total = sum(t.notional_usd for t in found)
    table = Table(
        title=f"🐋 Trades > ${min_usd:,.0f} (last {hours:g}h) — "
              f"${total:,.0f} total"
    )
    table.add_column("When", style="dim", justify="right")
    table.add_column("Value", style="bold green", justify="right")
    table.add_column("Side", justify="center")
    table.add_column("Outcome", style="cyan")
    table.add_column("Price", justify="right")
    table.add_column("Market", max_width=38, overflow="fold")
    table.add_column("Trader", style="magenta", max_width=14, overflow="fold")

    for trade in found:
        side_color = "green" if trade.side == "BUY" else "red"
        table.add_row(
            _fmt_age(trade.timestamp),
            f"${trade.notional_usd:,.0f}",
            f"[{side_color}]{safe(trade.side)}[/{side_color}]",
            safe(trade.outcome),
            f"${trade.price:.3f}",
            safe(trade.title),
            safe(trade.trader),
        )
    console.print(table)
    console.print(
        "[dim]Value = shares × price. A large trade is a sign of conviction, "
        "not a guarantee — it may be a hedge or market making.[/dim]"
    )


@app.command(rich_help_panel="Flow & Smart Money")
def leaderboard(
    category: str = typer.Option("OVERALL", "--category", "-c",
                                 help="OVERALL, POLITICS, SPORTS, CRYPTO…"),
    period: str = typer.Option("MONTH", "--period", "-p", help="DAY, WEEK, MONTH, ALL."),
    by: str = typer.Option("PNL", "--by", help="PNL or VOL."),
    limit: int = typer.Option(15, "--limit", "-l", min=1, max=50),
) -> None:
    """🏆 Most profitable traders — the smart-money starting point."""
    try:
        traders = whale_api.leaderboard(category, period, by, limit)
    except ApiError as exc:
        raise fail(str(exc))
    if not traders:
        console.print("[yellow]Leaderboard is empty.[/yellow]")
        return

    table = Table(title=f"🏆 Top traders — {safe(category.upper())} / {safe(period.upper())} by {safe(by.upper())}")
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Trader", style="cyan", max_width=24, overflow="fold")
    table.add_column("P&L", justify="right")
    table.add_column("Volume", justify="right", style="magenta")
    table.add_column("Wallet", style="dim", max_width=16, overflow="fold")

    for trader in traders:
        color = "green" if trader.pnl >= 0 else "red"
        table.add_row(
            str(trader.rank),
            safe(trader.name),
            f"[{color}]${trader.pnl:+,.0f}[/{color}]",
            f"${trader.volume:,.0f}",
            safe(keystore.short_address(trader.wallet)),
        )
    console.print(table)
    console.print(
        "[dim]Inspect one of them with: poly trader <wallet>[/dim]"
    )


@app.command(rich_help_panel="Flow & Smart Money")
def trader(
    wallet: str = typer.Argument(..., help="Wallet address (0x…)."),
    limit: int = typer.Option(10, "--limit", "-l", min=1, max=100),
) -> None:
    """🔍 A trader's profile: bankroll, positions and recent trades."""
    wallet = wallet.strip()
    if not (wallet.startswith("0x") and len(wallet) == 42):
        raise fail("invalid address (expected 0x + 40 hex).")

    try:
        value = whale_api.trader_value(wallet)
        positions_rows = whale_api.trader_positions(wallet, limit)
        trades_rows = whale_api.trader_trades(wallet, limit)
    except ApiError as exc:
        raise fail(str(exc))

    header = f"[bold]{safe(wallet)}[/bold]"
    if value is not None:
        header += f"\nValue in positions: [bold green]${value:,.2f}[/bold green]"
    console.print(Panel(header, title="🔍 Trader", border_style="cyan"))

    if positions_rows:
        table = Table(title="Current positions")
        table.add_column("Market", style="cyan", max_width=40, overflow="fold")
        table.add_column("Outcome")
        table.add_column("Value", justify="right")
        table.add_column("Avg price", justify="right")
        table.add_column("Current", justify="right")
        table.add_column("P&L", justify="right")
        for row in positions_rows:
            pnl = float(row.get("cashPnl") or 0.0)
            color = "green" if pnl >= 0 else "red"
            table.add_row(
                safe(row.get("title") or "?"),
                safe(row.get("outcome") or "?"),
                f"${float(row.get('currentValue') or 0):,.0f}",
                f"${float(row.get('avgPrice') or 0):.3f}",
                f"${float(row.get('curPrice') or 0):.3f}",
                f"[{color}]${pnl:+,.0f}[/{color}]",
            )
        console.print(table)
    else:
        console.print("[yellow]No open positions.[/yellow]")

    if trades_rows:
        table = Table(title="Recent trades")
        table.add_column("When", style="dim", justify="right")
        table.add_column("Value", justify="right")
        table.add_column("Side", justify="center")
        table.add_column("Outcome", style="cyan")
        table.add_column("Market", max_width=44, overflow="fold")
        for trade in trades_rows:
            color = "green" if trade.side == "BUY" else "red"
            table.add_row(
                _fmt_age(trade.timestamp),
                f"${trade.notional_usd:,.0f}",
                f"[{color}]{safe(trade.side)}[/{color}]",
                safe(trade.outcome),
                safe(trade.title),
            )
        console.print(table)


@app.command(rich_help_panel="Flow & Smart Money")
def holders(
    condition_id: str = typer.Argument(..., help="Market conditionId (0x…)."),
    limit: int = typer.Option(10, "--limit", "-l", min=1, max=20),
) -> None:
    """👥 Largest holders of each market outcome."""
    try:
        groups = whale_api.market_holders(condition_id, limit)
    except ApiError as exc:
        raise fail(str(exc))
    if not groups:
        console.print("[yellow]No holders found.[/yellow]")
        return

    for group in groups:
        rows = group.get("holders") or []
        if not rows:
            continue
        outcome = "?"
        for row in rows:
            if isinstance(row, dict) and row.get("outcomeIndex") is not None:
                outcome = f"outcome #{row.get('outcomeIndex')}"
                break
        table = Table(title=f"👥 Largest holders — {safe(outcome)}")
        table.add_column("Trader", style="cyan", max_width=26, overflow="fold")
        table.add_column("Shares", justify="right")
        table.add_column("Wallet", style="dim", max_width=16, overflow="fold")
        for row in rows:
            if not isinstance(row, dict):
                continue
            name = row.get("name") or row.get("pseudonym") or "?"
            table.add_row(
                safe(name),
                f"{float(row.get('amount') or 0):,.0f}",
                safe(keystore.short_address(row.get("proxyWallet"))),
            )
        console.print(table)


@app.command(rich_help_panel="Markets")
def quote(
    market_id: str = typer.Argument(..., help="Numeric ID or market slug."),
) -> None:
    """💹 Spread and top of book — what it costs to get in and out."""
    try:
        found = whale_api.quote_for(market_id)
    except ApiError as exc:
        raise fail(str(exc))
    if not found:
        raise fail(f"market not found: {market_id}")

    console.print(Panel(safe(found.question), border_style="cyan"))
    table = Table(show_header=False)
    table.add_column("", style="cyan")
    table.add_column("", justify="right")
    table.add_row("Best bid", f"${found.best_bid:.3f}")
    table.add_row("Best ask", f"${found.best_ask:.3f}")
    table.add_row("Spread", f"${found.spread:.3f} ({found.spread_pct:.1f}%)")
    table.add_row("Last trade", f"${found.last_trade:.3f}")
    table.add_row("24h volume", f"${found.volume_24h:,.0f}")
    table.add_row("Liquidity", f"${found.liquidity:,.0f}")
    console.print(table)

    if found.spread_pct > 10:
        console.print(
            "[yellow]⚠ Wide spread: getting in and out is expensive. "
            "The screen price is not the price you can actually get.[/yellow]"
        )


@app.command(rich_help_panel="Flow & Smart Money")
def alerts_reset() -> None:
    """Forget already-sent alerts (resumes notifying about old trades)."""
    if alerts.reset_state():
        console.print("[green]✔ Alert history cleared.[/green]")
    else:
        console.print("[yellow]There was no alert history.[/yellow]")


# ══════════════════════════════════════════════════════════════════════════════
# WALLET
# ══════════════════════════════════════════════════════════════════════════════


@app.command(rich_help_panel="Wallet")
def balance() -> None:
    """USDC balance available to trade."""
    try:
        value = trading.get_balance()
    except trading.TradingError as exc:
        raise fail(str(exc))
    if value is None:
        raise fail("the exchange did not return a balance.")
    console.print(Panel(f"[bold green]${value:,.2f} USDC[/bold green]",
                        title="Balance", border_style="green"))


@app.command(rich_help_panel="Wallet")
def positions() -> None:
    """Open positions and unrealized P&L."""
    try:
        rows = trading.get_positions()
    except trading.TradingError as exc:
        raise fail(str(exc))

    if not rows:
        console.print("[yellow]No open positions.[/yellow]")
        return

    table = Table(title="Positions")
    table.add_column("Market", style="cyan", max_width=44, overflow="fold")
    table.add_column("Outcome", style="white")
    table.add_column("Qty", justify="right")
    table.add_column("Avg price", justify="right")
    table.add_column("Current", justify="right")
    table.add_column("P&L", justify="right")

    total = 0.0
    for row in rows:
        pnl = float(row.get("cashPnl") or 0.0)
        total += pnl
        color = "green" if pnl >= 0 else "red"
        table.add_row(
            safe(row.get("title") or row.get("slug") or "?"),
            safe(row.get("outcome") or "?"),
            f"{float(row.get('size') or 0):,.2f}",
            f"${float(row.get('avgPrice') or 0):.3f}",
            f"${float(row.get('curPrice') or 0):.3f}",
            f"[{color}]${pnl:+,.2f}[/{color}]",
        )
    console.print(table)
    color = "green" if total >= 0 else "red"
    console.print(f"Total P&L: [{color}]${total:+,.2f}[/{color}]")


@app.command(rich_help_panel="Wallet")
def orders() -> None:
    """Open orders on the exchange."""
    try:
        rows = trading.get_open_orders()
    except trading.TradingError as exc:
        raise fail(str(exc))
    if not rows:
        console.print("[yellow]No open orders.[/yellow]")
        return
    table = Table(title="Open orders")
    for col in ("ID", "Side", "Price", "Size", "Remaining", "Status"):
        table.add_column(col)
    for row in rows:
        table.add_row(
            safe(str(row.get("id", ""))[:16]),
            safe(row.get("side", "")),
            f"${float(row.get('price') or 0):.3f}",
            f"{float(row.get('original_size') or 0):,.2f}",
            f"{float(row.get('size_matched') or 0):,.2f}",
            safe(row.get("status", "")),
        )
    console.print(table)


# ══════════════════════════════════════════════════════════════════════════════
# TRADING
# ══════════════════════════════════════════════════════════════════════════════


def _execute(side: str, token_id: str, price: float, size: float,
             yes: bool, market_label: str) -> None:
    settings = load_settings()

    # Kill switch takes precedence over everything — doesn't even authenticate.
    if guardrails.halt_active():
        raise fail(
            f"KILL SWITCH active ({halt_path()}). No order is evaluated. "
            "Clear it with `poly resume`."
        )

    balance_usd: Optional[float] = None
    open_orders: Optional[int] = None
    # Only reaches out to the exchange if a credential exists — avoids a
    # network round-trip (and deriving API credentials) when the order would
    # be blocked anyway.
    if keystore.keystore_exists() or os.environ.get(keystore.LEGACY_KEY_ENV):
        try:
            balance_usd = trading.get_balance(settings)
        except trading.TradingError:
            pass  # the guard-rail warns that the bankroll % could not be checked
        try:
            live = trading.get_open_orders(settings)
            open_orders = len(live)
            # The exchange is the source of truth: close in the journal
            # whatever it no longer lists, or the open-order counter only grows.
            journal.reconcile_open_orders(
                str(o.get("id") or o.get("orderID") or "") for o in live
            )
        except trading.TradingError:
            pass  # falls back to the journal

    decision = guardrails.evaluate_order(
        side, price, size, settings, balance_usd, open_orders
    )

    console.print(
        Panel(
            f"[bold]{side}[/bold] {size:g} shares @ ${price:.3f}\n"
            f"Cost: [bold]${decision.notional:.2f}[/bold] USDC"
            + (f"\nMarket: {safe(market_label)}" if market_label else "")
            + (f"\nBalance: ${balance_usd:,.2f}" if balance_usd is not None else ""),
            title="Proposed order",
            border_style="cyan",
        )
    )

    for warning in decision.warnings:
        console.print(f"  [yellow]⚠[/yellow] {safe(warning)}")

    if not decision.allowed:
        for reason in decision.reasons:
            console.print(f"  [red]✘[/red] {safe(reason)}")
        raise typer.Exit(1)

    confirmed = yes
    if decision.requires_confirmation and not yes:
        if not sys.stdin.isatty():
            raise fail(
                "confirmation needed but there is no terminal. Use --yes "
                "deliberately, or enable autonomous mode with an expiry."
            )
        if not settings.dry_run:
            console.print(
                "[bold yellow]⚠ REAL order with real money. Irreversible.[/bold yellow]"
            )
        confirmed = typer.confirm("Confirm sending?", default=False)
        if not confirmed:
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit(0)

    try:
        result = trading.place_order(
            token_id, side, price, size, settings,
            market_label=market_label, balance_usd=balance_usd, confirmed=confirmed,
        )
    except trading.TradingError as exc:
        raise fail(str(exc))

    if not result.ok:
        raise fail(result.detail or "order rejected")

    if result.dry_run:
        console.print(f"[cyan]{safe(result.detail)}[/cyan]")
        console.print("[dim]To go live: poly config --key dry_run --value false[/dim]")
    else:
        console.print(
            f"[green]✔ Order sent.[/green] ID: {safe(result.order_id or '—')} "
            f"({safe(result.status)})"
        )


@app.command(rich_help_panel="Trading")
def buy(
    token_id: str = typer.Argument(..., help="The OUTCOME's token_id (see `poly market`)."),
    price: float = typer.Argument(..., help="Limit price per share (0.01–0.99)."),
    size: float = typer.Argument(..., help="Number of shares."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip interactive confirmation."),
    label: str = typer.Option("", "--label", help="Market label for the journal."),
) -> None:
    """Buy shares of an outcome (GTC limit order)."""
    _execute("BUY", token_id, price, size, yes, label)


@app.command(rich_help_panel="Trading")
def sell(
    token_id: str = typer.Argument(..., help="The OUTCOME's token_id."),
    price: float = typer.Argument(..., help="Limit price per share (0.01–0.99)."),
    size: float = typer.Argument(..., help="Number of shares."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip interactive confirmation."),
    label: str = typer.Option("", "--label", help="Market label for the journal."),
) -> None:
    """Sell shares of an outcome (GTC limit order)."""
    _execute("SELL", token_id, price, size, yes, label)


@app.command(rich_help_panel="Trading")
def cancel(
    order_id: str = typer.Argument("", help="Order ID. Empty with --all cancels every one."),
    all_orders: bool = typer.Option(False, "--all", help="Cancel every open order."),
) -> None:
    """Cancel open orders."""
    try:
        if all_orders:
            trading.cancel_all()
            console.print("[green]✔ All open orders were cancelled.[/green]")
        elif order_id:
            trading.cancel_order(order_id)
            console.print(f"[green]✔ Order {safe(order_id)} cancelled.[/green]")
        else:
            raise fail("provide an order_id or use --all.")
    except trading.TradingError as exc:
        raise fail(str(exc))


# ══════════════════════════════════════════════════════════════════════════════
# SAFETY
# ══════════════════════════════════════════════════════════════════════════════


@app.command(rich_help_panel="Safety")
def halt(reason: str = typer.Argument("", help="Reason recorded in the journal.")) -> None:
    """EMERGENCY STOP: blocks every order until `poly resume`."""
    guardrails.engage_halt(reason)
    console.print(
        Panel(
            "[bold red]KILL SWITCH ACTIVE[/bold red]\n\n"
            "No order will be sent, not even in autonomous mode.\n"
            f"File: {safe(halt_path())}\n\n"
            "Release with [cyan]poly resume[/cyan].",
            border_style="red",
        )
    )


@app.command(rich_help_panel="Safety")
def resume() -> None:
    """Release the kill switch."""
    if guardrails.release_halt():
        console.print("[green]✔ Kill switch released. Orders are evaluated again.[/green]")
    else:
        console.print("[yellow]The kill switch was not active.[/yellow]")


@app.command(rich_help_panel="Safety")
def auto(
    enable: bool = typer.Argument(..., help="true to enable, false to disable."),
    hours: float = typer.Option(1.0, "--hours", min=0.25, max=24.0,
                                help="Validity in hours (max 24)."),
    acknowledge: bool = typer.Option(
        False, "--i-understand-the-risk",
        help="Required to ENABLE: confirms awareness of the financial risk.",
    ),
) -> None:
    """Enable/disable autonomous mode (orders placed unattended, WITH an expiry).

    Even enabled, every financial cap still applies and the kill switch
    still takes precedence.
    """
    settings = load_settings()

    if not enable:
        save_settings(guardrails.disable_autonomous(settings))
        console.print("[green]✔ Autonomous mode disabled. Every order will ask for confirmation.[/green]")
        return

    if not acknowledge:
        raise fail(
            "enabling autonomous mode requires --i-understand-the-risk. "
            "In this mode the agent sends real-money orders unattended."
        )
    if settings.dry_run is False and settings.max_position_usd > 100:
        console.print(
            "[yellow]⚠ Per-order cap above $100 with dry-run off.[/yellow]"
        )

    save_settings(guardrails.enable_autonomous(settings, hours))
    console.print(
        Panel(
            f"[bold red]AUTONOMOUS MODE ENABLED for {hours:g}h[/bold red]\n\n"
            f"Per-order cap: ${settings.max_position_usd:.2f}\n"
            f"Daily cap: ${settings.max_daily_spend_usd:.2f}\n"
            f"Dry-run: {'ON (nothing is sent)' if settings.dry_run else 'OFF — real orders'}\n\n"
            "Expires on its own. Cut it short with [cyan]poly auto false[/cyan] "
            "or [cyan]poly halt[/cyan].",
            border_style="red",
        )
    )


@app.command(rich_help_panel="Safety")
def history(limit: int = typer.Option(20, "--limit", "-l", min=1, max=200)) -> None:
    """Audit trail: everything the skill has attempted to do with money."""
    rows = journal.recent(limit)
    if not rows:
        console.print("[yellow]Journal is empty — no order recorded.[/yellow]")
        return
    table = Table(title="Audit trail")
    for col in ("When", "Kind", "Status", "Side", "Price", "Notional", "Detail"):
        table.add_column(col, overflow="fold")
    colors = {
        "filled": "green", "submitted": "cyan", "dry_run": "blue",
        "rejected": "yellow", "failed": "red", "cancelled": "dim",
    }
    for row in rows:
        status = str(row.get("status", ""))
        color = colors.get(status, "white")
        table.add_row(
            safe(str(row.get("at", ""))[:19]),
            safe(row.get("kind", "")),
            f"[{color}]{safe(status)}[/{color}]",
            safe(row.get("side", "")),
            f"${float(row.get('price') or 0):.3f}" if row.get("price") else "",
            f"${float(row.get('notional') or 0):.2f}" if row.get("notional") else "",
            safe(str(row.get("detail", ""))[:60]),
        )
    console.print(table)
    console.print(f"[dim]Spend in the last 24h: ${journal.spend_since(86400):.2f}[/dim]")


@app.command(rich_help_panel="Safety")
def revoke(
    yes: bool = typer.Option(False, "--yes", "-y", help="Don't ask."),
) -> None:
    """Delete the local keystore (the on-chain wallet is not affected)."""
    if not keystore.keystore_exists():
        console.print("[yellow]No keystore to remove.[/yellow]")
        return
    if not yes and sys.stdin.isatty():
        if not typer.confirm("Delete the encrypted keystore on this machine?", default=False):
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit(0)
    keystore.delete_key()
    console.print("[green]✔ Keystore removed.[/green]")
    console.print(
        "[dim]The funds remain in the on-chain wallet. To truly revoke access, "
        "move the balance to another wallet.[/dim]"
    )


@app.command(rich_help_panel="Setup")
def version() -> None:
    """Skill version."""
    console.print(f"polymarket-agent {__version__}")


# `markets` is the name of an imported module; register the command under the
# public name.
app.command(name="markets", rich_help_panel="Markets")(markets_cmd)


def main() -> None:
    try:
        app()
    except KeyboardInterrupt:  # pragma: no cover
        err_console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(130)


if __name__ == "__main__":  # pragma: no cover
    main()
