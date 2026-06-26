#!/usr/bin/env python3
"""
MoneySharks interactive onboarding CLI.
Guides the user through collecting credentials and config, presents the consent gate,
writes config.json, and optionally starts the first trading cycle.

usage: onboarding.py [--output config.json] [--non-interactive]

Set ASTER_API_KEY and ASTER_API_SECRET in your shell before running,
or provide them when prompted (they will NOT be written to config.json).
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE.parent / "config.json"


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", file=sys.stderr)


def run_json(args: list, stdin_obj=None) -> dict:
    try:
        proc = subprocess.run(
            args,
            input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
        return json.loads(proc.stdout.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def ask(prompt: str, default: str = "") -> str:
    if default:
        val = input(f"  {prompt} [{default}]: ").strip()
        return val if val else default
    else:
        while True:
            val = input(f"  {prompt}: ").strip()
            if val:
                return val
            print("  (required — please enter a value)")


def ask_float(prompt: str, default: float) -> float:
    while True:
        val = input(f"  {prompt} [{default}]: ").strip()
        if not val:
            return default
        try:
            return float(val)
        except ValueError:
            print("  (please enter a number)")


def ask_int(prompt: str, default: int) -> int:
    while True:
        val = input(f"  {prompt} [{default}]: ").strip()
        if not val:
            return default
        try:
            return int(val)
        except ValueError:
            print("  (please enter an integer)")


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]


def test_credentials(api_key: str, api_secret: str) -> bool:
    """Try a read-only account call to verify credentials work."""
    env = dict(os.environ)
    env["ASTER_API_KEY"] = api_key
    env["ASTER_API_SECRET"] = api_secret
    try:
        proc = subprocess.run(
            [sys.executable, str(BASE / "aster_readonly_client.py"), "account"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
            env=env,
            check=False,
        )
        result = json.loads(proc.stdout.decode())
        # Aster /fapi/v2/account returns a dict with 'totalWalletBalance'
        return "totalWalletBalance" in result or "assets" in result
    except Exception:
        return False


def build_config(
    symbols: list[str],
    base_value: float,
    max_leverage: int,
    min_leverage: int = 2,
    max_daily_loss: float = None,
    max_total_exposure: float = None,
    allow_short: bool = True,
    scan_interval: int = 2,
    mode: str = "autonomous_live",
    consent: bool = True,
) -> dict:
    """Build a full config dict with all defaults applied."""
    max_notional = base_value * max_leverage
    total_exposure = max_total_exposure or (base_value * 10)
    daily_loss = max_daily_loss or (total_exposure * 0.10)

    return {
        "mode": mode,
        "autonomous_live_consent": consent and mode == "autonomous_live",
        "allowed_symbols": symbols,
        "base_value_per_trade": base_value,
        "risk_pct_per_trade": 0.01,
        "min_leverage": min_leverage,
        "max_leverage": max_leverage,
        "max_notional_per_trade": round(max_notional, 2),
        "max_total_exposure": round(total_exposure, 2),
        "max_concurrent_positions": 3,
        "max_daily_loss": round(daily_loss, 2),
        "allow_short": allow_short,
        "require_stop_loss": True,
        "require_take_profit": True,
        "min_reward_risk": 1.5,
        "cooldown_after_close_sec": 120,
        "minimum_hold_sec": 60,
        "cron": {
            "enabled": mode == "autonomous_live" and consent,
            "scan_interval_minutes": scan_interval,
            "review_interval_minutes": 30,
            "daily_summary_hour": 0,
        },
        "sentiment": {
            "enabled": False,
            "weight": 0.1,
        },
        "execution": {
            "cancel_on_halt": True,
            "flatten_on_emergency_stop": False,
            "require_human_approval_for_live_orders": False,
        },
    }


def print_consent_gate(
    symbols: list[str],
    base_value: float,
    min_lev: int,
    max_lev: int,
    max_daily_loss: float,
    max_exposure: float,
    scan_interval: int,
) -> None:
    symbols_str = ", ".join(symbols)
    print()
    print("━" * 66)
    print("⚠️  AUTONOMOUS LIVE TRADING — READ CAREFULLY BEFORE ACCEPTING")
    print("━" * 66)
    print()
    print("  Your setup summary:")
    print(f"    • Symbols:           {symbols_str}")
    print(f"    • Base investment:   ${base_value:,.2f} per trade")
    print(f"    • Leverage:          {min_lev}× – {max_lev}×")
    print(f"    • Max daily loss:    ${max_daily_loss:,.2f}")
    print(f"    • Max total exposure:${max_exposure:,.2f}")
    print(f"    • Scan interval:     every {scan_interval} minutes")
    print()
    print("  By typing ACCEPT below, you authorise MoneySharks to:")
    print()
    print("    • Place and manage REAL leveraged orders on Aster DEX")
    print("      using your API credentials, 24 hours a day, 7 days a week.")
    print("    • Execute trades automatically WITHOUT asking for your")
    print("      approval on each individual trade.")
    print("    • Manage, modify, and close open positions autonomously.")
    print("    • Operate continuously via background cron until you halt it.")
    print()
    print("  Hard safeguards always active:")
    print("    • Max daily loss cap            ✓")
    print("    • Stop-loss on every trade      ✓")
    print("    • Take-profit on every trade    ✓")
    print("    • Leverage capped at max        ✓")
    print("    • Circuit breakers              ✓")
    print()
    print("  To stop at any time, say:")
    print('    "halt moneysharks" / "kill switch" / "switch to paper mode"')
    print('    or: python3 scripts/halt.py config.json --cancel-orders')
    print()
    print("  ⚠  Futures trading is HIGH RISK. You may lose your entire")
    print("      deposit. Past performance does not guarantee future results.")
    print()
    print("━" * 66)


def main() -> int:
    config_path = DEFAULT_CONFIG_PATH
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        config_path = Path(sys.argv[idx + 1])

    non_interactive = "--non-interactive" in sys.argv

    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║   🦈  MoneySharks — Onboarding Wizard           ║")
    print("║   Autonomous 24/7 Aster Futures Trading Agent   ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    print("  I need just a few things to get you set up.")
    print()

    # ── Credentials ──
    print("── Step 1: Aster API Credentials ──────────────────")
    print()
    print("  ⚠ Credentials will be stored in your shell environment,")
    print("    NOT written to config.json.")
    print()

    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")

    if api_key and api_secret:
        print(f"  ✓ ASTER_API_KEY already set:    ****{api_key[-4:]}")
        print(f"  ✓ ASTER_API_SECRET already set: ****{api_secret[-4:]}")
        print()
    else:
        print("  ASTER_API_KEY and ASTER_API_SECRET are not set in your environment.")
        print("  Please set them now:")
        print()
        api_key = ask("Aster API key")
        api_secret = ask("Aster API secret")
        print()
        print(f"  ✓ Key:    ****{api_key[-4:]}")
        print(f"  ✓ Secret: ****{api_secret[-4:]}")
        print()
        print("  ⚠ To persist credentials across sessions, set them in your environment.")
        print("    Use a secrets manager or a private, permission-restricted env file.")
        print("    Avoid embedding raw keys directly in shell profile files (~/.zshrc etc.).")
        print()

    # ── Validate credentials ──
    print("  Verifying credentials against Aster API ...")
    orig_key = os.environ.get("ASTER_API_KEY")
    orig_secret = os.environ.get("ASTER_API_SECRET")
    os.environ["ASTER_API_KEY"] = api_key
    os.environ["ASTER_API_SECRET"] = api_secret
    creds_ok = test_credentials(api_key, api_secret)
    if not creds_ok:
        if orig_key is None:
            os.environ.pop("ASTER_API_KEY", None)
        if orig_secret is None:
            os.environ.pop("ASTER_API_SECRET", None)
        print()
        print("  ✗ Credential verification FAILED.")
        print("    Check your API key/secret and ensure Futures trading is enabled.")
        print("    You can re-run onboarding.py after correcting the credentials.")
        return 1

    print("  ✓ Credentials verified successfully.")
    print()

    # ── Symbols ──
    print("── Step 2: Trading Configuration ──────────────────")
    print()
    raw_symbols = ask(
        "Symbols to trade (space or comma separated)",
        "BTCUSDT ETHUSDT SOLUSDT",
    )
    symbols = [s.strip().upper() for s in raw_symbols.replace(",", " ").split() if s.strip()]
    if not symbols:
        symbols = ["BTCUSDT"]
    print(f"  ✓ Symbols: {', '.join(symbols)}")
    print()

    base_value = ask_float("Base investment per trade in USD (e.g. 100)", 100.0)
    max_leverage = ask_int("Max leverage (e.g. 10)", 10)
    min_leverage = ask_int("Min leverage (e.g. 2)", 2)

    if min_leverage > max_leverage:
        print(f"  ⚠ min_leverage ({min_leverage}) > max_leverage ({max_leverage}). Setting min=2.")
        min_leverage = min(2, max_leverage)

    total_exposure_default = round(base_value * 10, 2)
    total_exposure = ask_float(f"Max total exposure in USD", total_exposure_default)
    daily_loss_default = round(total_exposure * 0.10, 2)
    max_daily_loss = ask_float(f"Max daily loss in USD", daily_loss_default)
    allow_short_str = ask("Allow short positions? (y/n)", "y")
    allow_short = allow_short_str.lower() in ("y", "yes", "1", "true")
    print()

    # ── Compute config ──
    config = build_config(
        symbols=symbols,
        base_value=base_value,
        max_leverage=max_leverage,
        min_leverage=min_leverage,
        max_daily_loss=max_daily_loss,
        max_total_exposure=total_exposure,
        allow_short=allow_short,
        scan_interval=2,
        mode="paper",  # start as paper until consent
        consent=False,
    )

    # ── Validate config ──
    validation = run_json([sys.executable, str(BASE / "validate_config.py")], config)
    if not validation.get("ok", True):
        print(f"  ✗ Config validation failed: {validation.get('errors')}")
        return 1
    if validation.get("warnings"):
        print("  ⚠ Warnings:")
        for w in validation["warnings"]:
            print(f"    - {w}")
        print()

    # ── Consent gate ──
    print_consent_gate(
        symbols=symbols,
        base_value=base_value,
        min_lev=min_leverage,
        max_lev=max_leverage,
        max_daily_loss=max_daily_loss,
        max_exposure=total_exposure,
        scan_interval=2,
    )

    if non_interactive:
        # --non-interactive ALWAYS declines autonomous_live consent.
        # It is intentionally impossible to grant autonomous_live consent
        # non-interactively — a human must physically type ACCEPT.
        print("  --non-interactive mode: consent defaults to DECLINE (paper mode).")
        print("  Autonomous live trading requires a manual human ACCEPT — it cannot be")
        print("  granted via flags, environment variables, or programmatic invocation.")
        consent_answer = "DECLINE"
    else:
        consent_answer = input("  Type ACCEPT or DECLINE: ").strip().upper()

    print()
    consented = consent_answer == "ACCEPT"

    if consented:
        config["mode"] = "autonomous_live"
        config["autonomous_live_consent"] = True
        config["cron"]["enabled"] = True
    else:
        config["mode"] = "paper"
        config["autonomous_live_consent"] = False
        config["cron"]["enabled"] = False

    # ── Write config.json ──
    config_path.write_text(json.dumps(config, indent=2))
    print(f"  ✓ config.json written to: {config_path}")

    # ── Generate cron job definitions ──
    cron_json_path = BASE.parent / "register_crons.json"
    crons_result = run_json([
        sys.executable, str(BASE / "register_crons.py"),
        str(config_path),
        "--skill-root", str(BASE.parent),
        "--mode", "autonomous_live" if consented else "paper",
        "--output", str(cron_json_path),
    ])
    if crons_result.get("ok"):
        print(f"  ✓ Cron job definitions written to: {cron_json_path}")
    else:
        print(f"  ⚠ Cron generation warning: {crons_result.get('error', 'unknown')}")

    if consented:
        print()
        print("✅  MoneySharks is configured for AUTONOMOUS LIVE trading.")
        print()
        print(f"  Trading:         {', '.join(symbols)}")
        print(f"  Leverage:        {min_leverage}× – {max_leverage}×")
        print(f"  Max daily loss:  ${max_daily_loss:,.2f}")
        print(f"  Max exposure:    ${total_exposure:,.2f}")
        print(f"  Scan interval:   every 2 minutes")
        print()
        print("  ── Next Steps ────────────────────────────────────────")
        print()
        print("  1. Set credentials in your environment (if not already):")
        print(f'     export ASTER_API_KEY="your-api-key"')
        print(f'     export ASTER_API_SECRET="your-api-secret"')
        print(f"     Use a secrets manager or a private env file; avoid storing raw keys in shell profiles.")
        print()
        print("  2. If using OpenClaw agent: say 'start moneysharks' or 'register moneysharks crons'.")
        print(f"     The agent will register the 4 cron jobs from: {cron_json_path}")
        print()
        print("  3. Run the first cycle to verify everything works:")
        print(f"     python3 {BASE}/autonomous_runner.py {config_path}")
        print()
        print("  4. Check status at any time:")
        print(f"     python3 {BASE}/status.py {config_path}")
        print()
        print("  ── Emergency Controls ────────────────────────────────")
        print()
        print('  Stop all trading:  python3 scripts/halt.py config.json --cancel-orders')
        print('  Or say:            "halt moneysharks" / "kill switch"')
        print('  Resume safely:     python3 scripts/resume.py config.json --mode paper')
        print()
        print("  ── Cron Jobs Registered ──────────────────────────────")
        print()
        if crons_result.get("active_jobs"):
            for job in crons_result["active_jobs"]:
                job_def = crons_result.get("cron_jobs", {}).get(job, {})
                schedule = job_def.get("schedule", {})
                sched_str = schedule.get("expr") or schedule.get("at") or schedule.get("everyMs")
                print(f"  • {job:<35s} [{sched_str}]")
        print()
    else:
        print()
        print("📝  Running in PAPER mode — no real orders will be placed.")
        print()
        print("  Run the first simulation cycle:")
        print(f"     python3 {BASE}/autonomous_runner.py {config_path}")
        print()
        print("  Check paper trading status:")
        print(f"     python3 {BASE}/status.py {config_path}")
        print()
        print("  When ready to go live, re-run onboarding.py and type ACCEPT.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
