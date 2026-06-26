#!/usr/bin/env python3
"""Query GMNCODE usage data via HTTP APIs.

Secure credential loading order:
1. Environment variables: GMNCODE_EMAIL / GMNCODE_PASSWORD
2. ~/.openclaw/.env entries with the same names

Base URL is hardcoded to https://gmncode.cn because it is not sensitive.

Features:
- Login on demand and cache token locally with restrictive permissions
- Retry automatically on 401/INVALID_TOKEN by re-login
- Query dashboard stats / trend / per-model usage
- Query active subscriptions and derive daily account quota metrics

Examples:
  python3 gmncode_usage.py report --date today
  python3 gmncode_usage.py quota
  python3 gmncode_usage.py brief
  python3 gmncode_usage.py report --date 2026-03-25
  python3 gmncode_usage.py report --start 2026-03-01 --end 2026-03-26
  python3 gmncode_usage.py models --date 2026-03-25 --json
  python3 gmncode_usage.py stats --json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

TIMEZONE = "Asia/Shanghai"
DEFAULT_BASE_URL = "https://gmncode.cn"
ENV_FILE = pathlib.Path.home() / ".openclaw" / ".env"
CACHE_DIR = pathlib.Path.home() / ".cache" / "openclaw" / "gmncode-usage"
TOKEN_CACHE = CACHE_DIR / "token.json"


def load_dotenv(path: pathlib.Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value
    return data


def env_value(key: str, dotenv: dict[str, str]) -> str | None:
    return os.environ.get(key) or dotenv.get(key)


def ensure_file_mode(path: pathlib.Path, mode: int) -> None:
    try:
        path.chmod(mode)
    except OSError:
        pass


def secure_write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    ensure_file_mode(path, stat.S_IRUSR | stat.S_IWUSR)


def load_credentials() -> tuple[str, str, str]:
    dotenv = load_dotenv(ENV_FILE)
    email = env_value("GMNCODE_EMAIL", dotenv)
    password = env_value("GMNCODE_PASSWORD", dotenv)
    base_url = DEFAULT_BASE_URL
    if not email or not password:
        raise SystemExit(
            "Missing GMNCODE credentials. Set GMNCODE_EMAIL and GMNCODE_PASSWORD "
            f"in environment variables or {ENV_FILE}."
        )
    return email, password, base_url.rstrip("/")


class GMNCodeClient:
    def __init__(self, email: str, password: str, base_url: str):
        self.email = email
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.api_base = f"{self.base_url}/api/v1"
        self.token: str | None = None
        self._load_cached_token()

    def _load_cached_token(self) -> None:
        if not TOKEN_CACHE.exists():
            return
        try:
            payload = json.loads(TOKEN_CACHE.read_text(encoding="utf-8"))
            token = payload.get("access_token")
            expires_at = payload.get("expires_at")
            if token and isinstance(expires_at, int):
                if int(dt.datetime.now(dt.timezone.utc).timestamp()) < expires_at - 60:
                    self.token = token
        except Exception:
            self.token = None

    def _save_cached_token(self, access_token: str, expires_in: int) -> None:
        expires_at = int(dt.datetime.now(dt.timezone.utc).timestamp()) + int(expires_in)
        secure_write_json(TOKEN_CACHE, {
            "access_token": access_token,
            "expires_at": expires_at,
            "base_url": self.base_url,
        })

    def clear_cached_token(self) -> None:
        self.token = None
        try:
            TOKEN_CACHE.unlink()
        except FileNotFoundError:
            pass

    def login(self) -> str:
        body = json.dumps({"email": self.email, "password": self.password}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.api_base}/auth/login",
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read())
        data = payload.get("data") or {}
        token = data.get("access_token")
        expires_in = int(data.get("expires_in") or 86400)
        if not token:
            raise RuntimeError(f"Login succeeded but no token returned: {payload}")
        self.token = token
        self._save_cached_token(token, expires_in)
        return token

    def ensure_token(self) -> str:
        if self.token:
            return self.token
        return self.login()

    def _request(self, path: str, params: dict[str, Any] | None = None, retry: bool = True) -> Any:
        query = urllib.parse.urlencode({k: v for k, v in (params or {}).items() if v is not None})
        url = f"{self.api_base}{path}"
        if query:
            url = f"{url}?{query}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.ensure_token()}",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh",
                "Referer": f"{self.base_url}/dashboard",
                "User-Agent": "Mozilla/5.0 OpenClaw GMNCode Usage Skill",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            if retry and exc.code == 401:
                self.clear_cached_token()
                self.login()
                return self._request(path, params=params, retry=False)
            raise RuntimeError(f"HTTP {exc.code} calling {path}: {body}") from exc

        if payload.get("code") in ("INVALID_TOKEN", 401) and retry:
            self.clear_cached_token()
            self.login()
            return self._request(path, params=params, retry=False)
        if payload.get("code") not in (0, "0", None):
            raise RuntimeError(f"API error calling {path}: {payload}")
        return payload.get("data")

    def dashboard_stats(self) -> dict[str, Any]:
        return self._request("/usage/dashboard/stats", params={"timezone": TIMEZONE})

    def dashboard_trend(self, start_date: str, end_date: str) -> dict[str, Any]:
        return self._request(
            "/usage/dashboard/trend",
            params={"start_date": start_date, "end_date": end_date, "timezone": TIMEZONE},
        )

    def dashboard_models(self, start_date: str, end_date: str) -> dict[str, Any]:
        return self._request(
            "/usage/dashboard/models",
            params={"start_date": start_date, "end_date": end_date, "timezone": TIMEZONE},
        )

    def active_subscriptions(self) -> list[dict[str, Any]]:
        return self._request("/subscriptions", params={"status": "active"}) or []


def parse_date_spec(value: str | None) -> tuple[str, str]:
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()
    if not value or value == "today":
        return today.isoformat(), today.isoformat()
    if value == "yesterday":
        d = today - dt.timedelta(days=1)
        return d.isoformat(), d.isoformat()
    if value == "this-month":
        return today.replace(day=1).isoformat(), today.isoformat()
    if "," in value:
        start, end = [part.strip() for part in value.split(",", 1)]
        return start, end
    return value, value


def fmt_tokens(value: int | float) -> str:
    n = float(value)
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


def derive_daily_quota(subscriptions: list[dict[str, Any]]) -> dict[str, float]:
    daily_limit = 0.0
    daily_used = 0.0
    for sub in subscriptions:
        group = sub.get("group") or {}
        daily_limit += float(group.get("daily_limit_usd") or 0)
        daily_used += float(sub.get("daily_usage_usd") or 0)
    return {
        "daily_limit_usd": daily_limit,
        "daily_used_usd": daily_used,
        "daily_remaining_usd": daily_limit - daily_used,
    }


def print_quota(client: GMNCodeClient) -> None:
    subs = client.active_subscriptions()
    quota = derive_daily_quota(subs)
    print("📊 账户额度")
    print(f"  每日使用额度: ${quota['daily_limit_usd']:.6f}")
    print(f"  今日已用:     ${quota['daily_used_usd']:.6f}")
    print(f"  今日剩余:     ${quota['daily_remaining_usd']:.6f}")


def print_brief(client: GMNCodeClient, date: str) -> None:
    subs = client.active_subscriptions()
    quota = derive_daily_quota(subs)
    models = client.dashboard_models(date, date).get("models", [])
    print("📊 账户额度")
    print(f"  每日使用额度: ${quota['daily_limit_usd']:.6f}")
    print(f"  今日已用:     ${quota['daily_used_usd']:.6f}")
    print(f"  今日剩余:     ${quota['daily_remaining_usd']:.6f}")
    print("\n🤖 今日模型使用")
    for model in models:
        print(
            f"  {model['model']}: {fmt_tokens(model['total_tokens'])} tokens | "
            f"actual ${float(model.get('actual_cost') or 0):.6f}"
        )


def print_report(client: GMNCodeClient, start_date: str, end_date: str) -> None:
    stats = client.dashboard_stats()
    trend = client.dashboard_trend(start_date, end_date)
    rows = trend.get("trend", [])
    range_requests = sum(int(day.get("requests") or 0) for day in rows)
    range_tokens = sum(int(day.get("total_tokens") or 0) for day in rows)
    range_cost = sum(float(day.get("cost") or 0) for day in rows)
    range_actual_cost = sum(float(day.get("actual_cost") or 0) for day in rows)

    print(f"📅 区间: {start_date} → {end_date}\n")
    print("📊 区间汇总")
    print(f"  区间请求:   {range_requests:,}")
    print(f"  区间 Tokens: {fmt_tokens(range_tokens)}")
    print(f"  区间费用:   ${range_cost:.4f} (actual ${range_actual_cost:.4f})")
    print(f"  当前今日:   {stats['today_requests']:,} 请求 | {fmt_tokens(stats['today_tokens'])} | ${stats['today_cost']:.4f}")
    print(f"  当前累计:   {stats['total_requests']:,} 请求 | {fmt_tokens(stats['total_tokens'])} | ${stats['total_cost']:.4f} (actual ${stats['total_actual_cost']:.4f})\n")

    print("📈 每日趋势")
    print(f"{'日期':<12} {'请求数':>8} {'Tokens':>10} {'费用':>10}")
    print("-" * 46)
    for day in rows:
        print(f"{day['date']:<12} {day['requests']:>8,} {fmt_tokens(day['total_tokens']):>10} ${day['cost']:>9.4f}")

    if start_date == end_date:
        models = client.dashboard_models(start_date, end_date).get("models", [])
        print("\n🤖 模型分布")
        for model in models:
            print(
                f"  {model['model']}: {model['requests']:,} 请求 | "
                f"{fmt_tokens(model['total_tokens'])} tokens | ${model['cost']:.4f}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Query GMNCODE dashboard usage APIs")
    sub = parser.add_subparsers(dest="command", required=False)

    p_stats = sub.add_parser("stats", help="Fetch dashboard aggregate stats")
    p_stats.add_argument("--json", action="store_true")

    p_trend = sub.add_parser("trend", help="Fetch daily trend")
    p_trend.add_argument("--date", default=None, help="today | yesterday | this-month | YYYY-MM-DD | start,end")
    p_trend.add_argument("--start")
    p_trend.add_argument("--end")
    p_trend.add_argument("--json", action="store_true")

    p_models = sub.add_parser("models", help="Fetch model usage for a single day or range")
    p_models.add_argument("--date", default="today", help="today | YYYY-MM-DD | start,end")
    p_models.add_argument("--start")
    p_models.add_argument("--end")
    p_models.add_argument("--json", action="store_true")

    p_report = sub.add_parser("report", help="Print combined report")
    p_report.add_argument("--date", default="today", help="today | yesterday | this-month | YYYY-MM-DD | start,end")
    p_report.add_argument("--start")
    p_report.add_argument("--end")

    p_quota = sub.add_parser("quota", help="Print account daily quota derived from active subscriptions")

    p_brief = sub.add_parser("brief", help="Print the concise metrics set: account daily quota + today model usage")
    p_brief.add_argument("--date", default="today", help="today | YYYY-MM-DD")

    args = parser.parse_args()
    email, password, base_url = load_credentials()
    client = GMNCodeClient(email=email, password=password, base_url=base_url)

    cmd = args.command or "report"
    if cmd == "stats":
        data = client.dashboard_stats()
        print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else data)
        return

    if cmd == "quota":
        print_quota(client)
        return

    if cmd == "brief":
        start_date, _ = parse_date_spec(getattr(args, "date", None))
        print_brief(client, start_date)
        return

    if cmd in {"trend", "models", "report"}:
        if getattr(args, "start", None) and getattr(args, "end", None):
            start_date, end_date = args.start, args.end
        else:
            start_date, end_date = parse_date_spec(getattr(args, "date", None))

        if cmd == "trend":
            data = client.dashboard_trend(start_date, end_date)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                for day in data.get("trend", []):
                    print(
                        f"{day['date']}\t{day['requests']}\t{day['total_tokens']}\t"
                        f"${day['cost']:.4f}"
                    )
            return

        if cmd == "models":
            data = client.dashboard_models(start_date, end_date)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                for model in data.get("models", []):
                    print(
                        f"{model['model']}\t{model['requests']}\t{model['total_tokens']}\t"
                        f"${model['cost']:.4f}"
                    )
            return

        print_report(client, start_date, end_date)
        return


if __name__ == "__main__":
    main()
