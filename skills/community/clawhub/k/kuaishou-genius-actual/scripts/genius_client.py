#!/usr/bin/env python3
"""
Genius API client for core business endpoints in management-yearly/actual flow.

Usage examples:
  python3 genius_client.py --cookie "accessproxy_session=xxx" user
  python3 genius_client.py --cookie "accessproxy_session=xxx" versions --year 2026
  python3 genius_client.py --cookie "accessproxy_session=xxx" detail --payload-file detail.json
  python3 genius_client.py --cookie "accessproxy_session=xxx" workflow --year 2026
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ApiResponse:
    ok: bool
    status: int
    url: str
    data: Any
    error: Optional[str] = None


class GeniusClient:
    def __init__(self, base_url: str, cookie: str, timeout: int = 20, insecure: bool = False):
        self.base_url = base_url.rstrip("/")
        self.cookie = cookie
        self.timeout = timeout
        self._ssl_ctx = None
        if insecure:
            self._ssl_ctx = ssl.create_default_context()
            self._ssl_ctx.check_hostname = False
            self._ssl_ctx.verify_mode = ssl.CERT_NONE

    def _request(self, method: str, path: str, *, query: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> ApiResponse:
        if not path.startswith("/"):
            path = "/" + path

        url = self.base_url + path
        if query:
            url += "?" + urllib.parse.urlencode(query, doseq=True)

        headers = {
            "Cookie": self.cookie,
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "genius-client/1.0",
        }
        data: Optional[bytes] = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url=url, method=method.upper(), headers=headers, data=data)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ssl_ctx) as resp:
                raw = resp.read()
                content_type = resp.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    parsed = json.loads(raw.decode("utf-8", errors="replace"))
                else:
                    parsed = raw.decode("utf-8", errors="replace")
                return ApiResponse(True, resp.status, url, parsed)
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
            return ApiResponse(False, e.code, url, raw, f"HTTPError {e.code}")
        except Exception as e:
            return ApiResponse(False, -1, url, "", f"{type(e).__name__}: {e}")

    # ----- Core APIs -----

    def get_user(self) -> ApiResponse:
        return self._request("GET", "/budget-portal/api/authority/user")

    def get_org_tree(self) -> ApiResponse:
        return self._request("GET", "/budget-portal/api/authority/org/tree")

    def get_horse_race(self, tab_code: str = "management-yearly/actual") -> ApiResponse:
        return self._request("GET", "/budget-portal/api/horse-race-lamp/query", query={"tabCode": tab_code})

    def get_latest_update_date(self) -> ApiResponse:
        return self._request("GET", "/budget-portal/api/description/act-latest-update-date")

    def get_versions(self, year: int) -> ApiResponse:
        return self._request("GET", "/budget-portal/api/annual-actual/versions", query={"year": year})

    def post_ledger_detail(self, payload: Dict[str, Any]) -> ApiResponse:
        return self._request("POST", "/budget-portal/api/actual-ledger/detail", body=payload)

    def post_ledger_products(self, payload: Dict[str, Any]) -> ApiResponse:
        return self._request("POST", "/budget-portal/api/actual-ledger/products", body=payload)


DEFAULT_DETAIL_PAYLOAD = {
    "year": 2026,
    "periodType": "MONTH",
}


def load_payload(path: Optional[str], fallback: Dict[str, Any], year: int) -> Dict[str, Any]:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    payload = dict(fallback)
    payload["year"] = year
    return payload


def print_response(resp: ApiResponse, pretty: bool = True) -> None:
    print(f"\n[{ 'OK' if resp.ok else 'ERR' }] {resp.status} {resp.url}")
    if resp.error:
        print(f"error: {resp.error}")

    if isinstance(resp.data, (dict, list)):
        if pretty:
            print(json.dumps(resp.data, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(resp.data, ensure_ascii=False))
    else:
        txt = str(resp.data)
        print(txt[:2000] + ("..." if len(txt) > 2000 else ""))


def run_workflow(client: GeniusClient, year: int, detail_payload: Dict[str, Any], products_payload: Dict[str, Any], pretty: bool) -> int:
    calls = [
        ("user", client.get_user),
        ("org_tree", client.get_org_tree),
        ("horse_race", client.get_horse_race),
        ("latest_update", client.get_latest_update_date),
        ("versions", lambda: client.get_versions(year)),
        ("detail", lambda: client.post_ledger_detail(detail_payload)),
        ("products", lambda: client.post_ledger_products(products_payload)),
    ]

    failed = 0
    for _, fn in calls:
        resp = fn()
        print_response(resp, pretty=pretty)
        if not resp.ok:
            failed += 1
    return failed


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Genius core API client")
    p.add_argument("command", choices=["user", "org-tree", "horse-race", "latest-update", "versions", "detail", "products", "workflow"], help="API command")
    p.add_argument("--base-url", default="https://genius.corp.kuaishou.com", help="Base URL")
    p.add_argument("--cookie", required=True, help="Cookie string, e.g. 'accessproxy_session=xxx; other=yyy'")
    p.add_argument("--year", type=int, default=2026, help="Year parameter")
    p.add_argument("--payload-file", help="JSON payload file for detail/products")
    p.add_argument("--products-payload-file", help="JSON payload file for products (workflow only)")
    p.add_argument("--timeout", type=int, default=20, help="HTTP timeout seconds")
    p.add_argument("--insecure", action="store_true", help="Disable TLS verification")
    p.add_argument("--compact", action="store_true", help="Compact JSON output")
    return p


def main() -> int:
    args = build_parser().parse_args()

    client = GeniusClient(
        base_url=args.base_url,
        cookie=args.cookie,
        timeout=args.timeout,
        insecure=args.insecure,
    )

    pretty = not args.compact

    if args.command == "user":
        print_response(client.get_user(), pretty=pretty)
    elif args.command == "org-tree":
        print_response(client.get_org_tree(), pretty=pretty)
    elif args.command == "horse-race":
        print_response(client.get_horse_race(), pretty=pretty)
    elif args.command == "latest-update":
        print_response(client.get_latest_update_date(), pretty=pretty)
    elif args.command == "versions":
        print_response(client.get_versions(args.year), pretty=pretty)
    elif args.command == "detail":
        payload = load_payload(args.payload_file, DEFAULT_DETAIL_PAYLOAD, args.year)
        print_response(client.post_ledger_detail(payload), pretty=pretty)
    elif args.command == "products":
        payload = load_payload(args.payload_file, DEFAULT_DETAIL_PAYLOAD, args.year)
        print_response(client.post_ledger_products(payload), pretty=pretty)
    elif args.command == "workflow":
        detail_payload = load_payload(args.payload_file, DEFAULT_DETAIL_PAYLOAD, args.year)
        products_payload = load_payload(args.products_payload_file, detail_payload, args.year)
        failed = run_workflow(client, args.year, detail_payload, products_payload, pretty=pretty)
        if failed:
            print(f"\nworkflow finished with {failed} failed call(s)")
            return 2
        print("\nworkflow finished successfully")
    else:
        raise ValueError("Unsupported command")

    return 0


if __name__ == "__main__":
    sys.exit(main())
