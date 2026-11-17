#!/usr/bin/env python3
"""Call one pay-per-call web tool at paypercall.dev and print one JSON object.

usage: python3 vend.py TOOL key=value [key=value ...] [--payment BLOCK_HASH]
       python3 vend.py --list

exit 0  the result is on stdout
exit 2  payment required: stdout is {"payment_required": {...}} with the amount and the account to pay
exit 3  the request was refused (bad parameter, unknown tool); nothing was charged
exit 4  the service did not answer; nothing was checked
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

MANIFEST = "https://extract.paypercall.dev/.well-known/x402"
USER_AGENT = "paypercall-web-tools-skill/1.0"
TIMEOUT_S = 60


def fetch(url, headers=None):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")


def tools():
    status, body = fetch(MANIFEST)
    if status != 200:
        raise OSError(f"manifest answered HTTP {status}")
    found = {}
    for resource in json.loads(body)["resources"]:
        name = resource["url"].rstrip("/").rsplit("/", 1)[-1]
        accept = resource["accepts"][0]
        found[name] = {"url": resource["url"], "amount_raw": accept["amount"], "pay_to": accept["payTo"],
                       "description": resource["description"]}
    return found


def main(argv):
    args = argv[1:]
    payment = None
    if "--payment" in args:
        at = args.index("--payment")
        payment = args[at + 1]
        del args[at:at + 2]
    try:
        catalogue = tools()
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"error": "service_unreachable", "detail": str(error)[:200]}))
        return 4
    if not args or args[0] == "--list":
        print(json.dumps({name: {"amount_raw": t["amount_raw"], "what": t["description"][:160]}
                          for name, t in sorted(catalogue.items())}, indent=1))
        return 0
    name, pairs = args[0], args[1:]
    if name not in catalogue or any("=" not in p for p in pairs):
        print(json.dumps({"error": "bad_request", "detail": "unknown tool or a parameter that is not key=value",
                          "tools": sorted(catalogue)}))
        return 3
    tool = catalogue[name]
    query = urllib.parse.urlencode([tuple(p.split("=", 1)) for p in pairs])
    headers = {"X-PAYMENT": payment} if payment else {}
    try:
        status, body = fetch(tool["url"] + ("?" + query if query else ""), headers)
    except OSError as error:
        print(json.dumps({"error": "service_unreachable", "detail": str(error)[:200]}))
        return 4
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = {"raw": body[:2000]}
    if status == 200:
        print(json.dumps(parsed))
        return 0
    if status == 402:
        print(json.dumps({"payment_required": {"amount_raw": tool["amount_raw"], "pay_to": tool["pay_to"],
                                               "network": "nano:mainnet", "asset": "XNO",
                                               "then": "send exactly amount_raw to pay_to, then rerun with --payment <send block hash>",
                                               "server_said": parsed.get("message", "")[:200] if isinstance(parsed, dict) else ""}}))
        return 2
    print(json.dumps({"error": "refused", "http_status": status, "detail": parsed}))
    return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
