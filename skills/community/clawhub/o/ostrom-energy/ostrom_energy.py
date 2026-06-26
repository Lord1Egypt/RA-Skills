#!/usr/bin/env python3
import argparse
import base64
import getpass
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone


def load_local_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        # Keep existing shell-provided variables as higher priority.
        os.environ.setdefault(key, value.strip())


def env_nonempty(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def load_home_config(config_dirname: str) -> dict:
    """
    Loads ~/.config/<config_dirname>/config.json if present.
    Credentials provided here can be shared safely across ClawHub installs
    without embedding secrets in the repo.
    """
    cfg_path = Path.home() / ".config" / config_dirname / "config.json"
    if not cfg_path.exists():
        return {}
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {cfg_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected object JSON in {cfg_path}.")
    return data


def config_get_str(cfg: dict, *keys: str) -> str | None:
    for k in keys:
        v = cfg.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            v = v.strip()
        else:
            v = str(v).strip()
        if v:
            return v
    return None


def prompt_value(label: str, is_secret: bool) -> str:
    if is_secret:
        return getpass.getpass(f"Enter {label}: ").strip()
    return input(f"Enter {label}: ").strip()


def resolve_credential(
    *,
    env_name: str,
    config: dict,
    config_keys: tuple[str, ...],
    prompt_missing: bool,
    prompt_label: str,
    is_secret: bool,
    default: str | None = None,
) -> str | None:
    env_value = env_nonempty(env_name)
    if env_value:
        return env_value

    cfg_value = config_get_str(config, *config_keys)
    if cfg_value:
        return cfg_value

    if prompt_missing:
        return prompt_value(prompt_label, is_secret=is_secret)

    return default


def parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def to_utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_access_token(client_id: str, client_secret: str, auth_base_url: str) -> str:
    url = auth_base_url.rstrip("/") + "/oauth2/token"
    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    basic = base64.b64encode(credentials).decode("ascii")
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    payload = request_json(req)
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"OAuth token missing in response: {payload}")
    return token


def fetch_spot_prices(
    token: str,
    api_base_url: str,
    start_date: datetime,
    end_date: datetime,
    zip_code: str | None,
):
    params = {
        "startDate": to_utc_iso(start_date),
        "endDate": to_utc_iso(end_date),
        "resolution": "HOUR",
    }
    if zip_code:
        params["zip"] = zip_code
    url = api_base_url.rstrip("/") + "/spot-prices?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    payload = request_json(req)

    points = []
    for row in payload.get("data", []):
        date = row.get("date")
        gross = row.get("grossKwhPrice")
        taxes = row.get("grossKwhTaxAndLevies")
        if date is None or gross is None:
            continue
        total_ct = float(gross) + float(taxes or 0.0)
        points.append(
            {
                "startsAt": date,
                "gross_ct_per_kwh": float(gross),
                "taxes_ct_per_kwh": float(taxes or 0.0),
                "total_ct_per_kwh": total_ct,
                "total_eur_per_kwh": total_ct / 100.0,
                "grossMonthlyOstromBaseFee": row.get("grossMonthlyOstromBaseFee"),
                "grossMonthlyGridFees": row.get("grossMonthlyGridFees"),
            }
        )
    points.sort(key=lambda x: x["startsAt"])
    return points


def request_json(req: urllib.request.Request) -> dict:
    max_attempts = 4
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < max_attempts:
                delay = min(2 ** (attempt - 1), 8)
                retry_after = exc.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    delay = max(delay, int(retry_after))
                time.sleep(delay)
                continue
            raise
        except urllib.error.URLError:
            if attempt < max_attempts:
                time.sleep(min(2 ** (attempt - 1), 8))
                continue
            raise
    raise RuntimeError("Failed to fetch JSON response after retries.")


def best_window(points, window_start, window_end, duration_hours):
    scoped = []
    for p in points:
        ts = parse_dt(p["startsAt"])
        if window_start and ts < window_start:
            continue
        if window_end and ts >= window_end:
            continue
        scoped.append({"ts": ts, **p})
    if len(scoped) < duration_hours:
        raise RuntimeError("Not enough hourly points in selected window.")

    best = None
    for i in range(0, len(scoped) - duration_hours + 1):
        chunk = scoped[i : i + duration_hours]
        contiguous = True
        for j in range(1, len(chunk)):
            if int((chunk[j]["ts"] - chunk[j - 1]["ts"]).total_seconds()) != 3600:
                contiguous = False
                break
        if not contiguous:
            continue
        total = sum(x["total_eur_per_kwh"] for x in chunk)
        if best is None or total < best["total"]:
            best = {"total": total, "chunk": chunk}
    if best is None:
        raise RuntimeError("No contiguous price window found.")
    return best


def command_prices(args, token, api_base_url, zip_code):
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=2)
    end = now + timedelta(hours=max(args.hours + 24, 48))
    points = fetch_spot_prices(token, api_base_url, start, end, zip_code)
    future = [p for p in points if parse_dt(p["startsAt"]).astimezone(timezone.utc) >= now]
    limited = future[: args.hours]
    print(f"Upcoming prices (next {len(limited)}h):")
    for p in limited:
        print(
            f"- {p['startsAt']}  "
            f"spot={p['gross_ct_per_kwh']:.3f} ct/kWh  "
            f"taxes={p['taxes_ct_per_kwh']:.3f} ct/kWh  "
            f"total={p['total_ct_per_kwh']:.3f} ct/kWh ({p['total_eur_per_kwh']:.4f} EUR/kWh)"
        )
    if limited:
        base_fee = limited[0].get("grossMonthlyOstromBaseFee")
        grid_fee = limited[0].get("grossMonthlyGridFees")
        if base_fee is not None or grid_fee is not None:
            print(
                "Monthly fixed fees (gross): "
                f"ostrom_base={base_fee if base_fee is not None else 'n/a'} EUR, "
                f"grid={grid_fee if grid_fee is not None else 'n/a'} EUR"
            )


def command_optimize(args, token, api_base_url, zip_code):
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=2)
    end = now + timedelta(days=4)
    points = fetch_spot_prices(token, api_base_url, start, end, zip_code)

    if args.duration_hours:
        duration = args.duration_hours
    else:
        if not args.kwh or not args.power_kw:
            raise RuntimeError("Provide either --duration-hours or both --kwh and --power-kw.")
        duration = math.ceil(args.kwh / args.power_kw)
        duration = max(duration, 1)

    ws = parse_dt(args.window_start) if args.window_start else None
    we = parse_dt(args.window_end) if args.window_end else None
    best = best_window(points, ws, we, duration)
    chunk = best["chunk"]
    avg_price = best["total"] / len(chunk)
    est_cost = (args.kwh * avg_price) if args.kwh else None
    print(f"Optimal {duration}h window:")
    print(f"- Start: {chunk[0]['startsAt']}")
    print(f"- End:   {chunk[-1]['startsAt']} +1h")
    print(f"- Avg price: {avg_price:.4f} EUR/kWh")
    if est_cost is not None:
        print(f"- Estimated energy cost ({args.kwh} kWh): {est_cost:.2f} EUR")
    print("Window details:")
    for p in chunk:
        print(
            f"  * {p['startsAt']} -> "
            f"{p['total_ct_per_kwh']:.3f} ct/kWh ({p['total_eur_per_kwh']:.4f} EUR/kWh)"
        )


def run_cmd(label: str, cmd: str, execute: bool):
    print(f"{label}: {cmd}")
    if execute:
        subprocess.run(cmd, shell=True, check=True)


def command_control(args, token, api_base_url, zip_code):
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=1)
    end = now + timedelta(hours=6)
    points = fetch_spot_prices(token, api_base_url, start, end, zip_code)
    future = [p for p in points if parse_dt(p["startsAt"]).astimezone(timezone.utc) <= now + timedelta(hours=1)]
    if not future:
        raise RuntimeError("No current/near-current price available.")
    current = future[-1]
    price = float(current["total_eur_per_kwh"])
    print(f"Current price: {price:.4f} EUR/kWh at {current.get('startsAt')}")
    execute = args.execute
    if not execute:
        print("Mode: dry-run (add --execute to run commands).")
    action_taken = False
    if args.price_below is not None and price <= args.price_below:
        if args.on_command:
            run_cmd("Price is below threshold -> ON command", args.on_command, execute)
            action_taken = True
    if args.price_above is not None and price >= args.price_above:
        if args.off_command:
            run_cmd("Price is above threshold -> OFF command", args.off_command, execute)
            action_taken = True
    if not action_taken:
        print("No threshold condition matched; no command executed.")


def build_parser():
    p = argparse.ArgumentParser(description="Ostrom energy helper for OpenClaw skill.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("prices", help="Show upcoming hourly spot prices.")
    s1.add_argument("--hours", type=int, default=24)
    s1.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    s2 = sub.add_parser("optimize", help="Find cheapest contiguous time window.")
    s2.add_argument("--duration-hours", type=int)
    s2.add_argument("--kwh", type=float)
    s2.add_argument("--power-kw", type=float)
    s2.add_argument("--window-start")
    s2.add_argument("--window-end")
    s2.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    s3 = sub.add_parser("control", help="Trigger commands from current price thresholds.")
    s3.add_argument("--price-below", type=float)
    s3.add_argument("--price-above", type=float)
    s3.add_argument("--on-command")
    s3.add_argument("--off-command")
    s3.add_argument("--execute", action="store_true")
    s3.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    return p


def main():
    load_local_env_file()
    parser = build_parser()
    args = parser.parse_args()

    prompt_missing = bool(getattr(args, "prompt_missing_secrets", False))
    config = load_home_config("ostrom-energy")

    client_id = resolve_credential(
        env_name="OSTROM_CLIENT_ID",
        config=config,
        config_keys=("client_id", "clientId", "OSTROM_CLIENT_ID"),
        prompt_missing=prompt_missing,
        prompt_label="OSTROM_CLIENT_ID",
        is_secret=False,
    )
    client_secret = resolve_credential(
        env_name="OSTROM_CLIENT_SECRET",
        config=config,
        config_keys=("client_secret", "clientSecret", "OSTROM_CLIENT_SECRET"),
        prompt_missing=prompt_missing,
        prompt_label="OSTROM_CLIENT_SECRET",
        is_secret=True,
    )
    zip_code = resolve_credential(
        env_name="OSTROM_ZIP",
        config=config,
        config_keys=("zip", "postal_code", "postalCode", "OSTROM_ZIP"),
        prompt_missing=prompt_missing,
        prompt_label="OSTROM_ZIP",
        is_secret=False,
        default=None,
    )

    ostrom_env = resolve_credential(
        env_name="OSTROM_ENV",
        config=config,
        config_keys=("env", "OSTROM_ENV"),
        prompt_missing=False,
        prompt_label="OSTROM_ENV",
        is_secret=False,
        default="production",
    )
    env = (ostrom_env or "production").lower()

    api_base_url = resolve_credential(
        env_name="OSTROM_API_BASE_URL",
        config=config,
        config_keys=("api_base_url", "OSTROM_API_BASE_URL"),
        prompt_missing=False,
        prompt_label="OSTROM_API_BASE_URL",
        is_secret=False,
        default=None,
    )
    auth_base_url = resolve_credential(
        env_name="OSTROM_AUTH_BASE_URL",
        config=config,
        config_keys=("auth_base_url", "OSTROM_AUTH_BASE_URL"),
        prompt_missing=False,
        prompt_label="OSTROM_AUTH_BASE_URL",
        is_secret=False,
        default=None,
    )

    if env == "sandbox":
        api_base_url = api_base_url or "https://sandbox.ostrom-api.io"
        auth_base_url = auth_base_url or "https://auth.sandbox.ostrom-api.io"
    else:
        api_base_url = api_base_url or "https://production.ostrom-api.io"
        auth_base_url = auth_base_url or "https://auth.production.ostrom-api.io"

    if not client_id or not client_secret:
        cfg_path = Path.home() / ".config" / "ostrom-energy" / "config.json"
        raise RuntimeError(
            "Missing OSTROM credentials. Set OSTROM_CLIENT_ID and OSTROM_CLIENT_SECRET "
            "as environment variables, or create config at "
            f"{cfg_path}. "
            "To be prompted interactively, rerun with --prompt-missing-secrets."
        )

    token = get_access_token(client_id, client_secret, auth_base_url)

    if args.cmd == "prices":
        command_prices(args, token, api_base_url, zip_code)
    elif args.cmd == "optimize":
        command_optimize(args, token, api_base_url, zip_code)
    elif args.cmd == "control":
        command_control(args, token, api_base_url, zip_code)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
