#!/usr/bin/env python3
"""headers — HTTP security headers checker. Zero dependencies."""
import urllib.request, sys, argparse, json

SECURITY_HEADERS = {
    "Strict-Transport-Security": {"severity": "high", "desc": "HSTS — force HTTPS"},
    "Content-Security-Policy": {"severity": "high", "desc": "CSP — prevent XSS/injection"},
    "X-Content-Type-Options": {"severity": "medium", "desc": "Prevent MIME sniffing", "expected": "nosniff"},
    "X-Frame-Options": {"severity": "medium", "desc": "Prevent clickjacking"},
    "Referrer-Policy": {"severity": "medium", "desc": "Control referrer info"},
    "Permissions-Policy": {"severity": "low", "desc": "Restrict browser features"},
    "X-XSS-Protection": {"severity": "low", "desc": "Legacy XSS filter"},
    "Cross-Origin-Opener-Policy": {"severity": "low", "desc": "Isolate browsing context"},
    "Cross-Origin-Resource-Policy": {"severity": "low", "desc": "Restrict resource loading"},
}

INFO_HEADERS = ["Server", "X-Powered-By", "X-AspNet-Version", "X-Generator"]

def check_url(url, timeout=10):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "headers-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            result = {"url": url, "status": resp.status, "present": [], "missing": [], "info_leak": [], "score": 0}
            total = len(SECURITY_HEADERS)
            for name, meta in SECURITY_HEADERS.items():
                if name.lower() in hdrs:
                    result["present"].append({"name": name, "value": hdrs[name.lower()], **meta})
                    result["score"] += 1
                else:
                    result["missing"].append({"name": name, **meta})
            for h in INFO_HEADERS:
                if h.lower() in hdrs:
                    result["info_leak"].append({"name": h, "value": hdrs[h.lower()]})
            result["grade"] = "A" if result["score"] >= 7 else "B" if result["score"] >= 5 else "C" if result["score"] >= 3 else "D" if result["score"] >= 1 else "F"
            result["score_pct"] = round(result["score"] / total * 100)
            return result
    except Exception as e:
        return {"url": url, "error": str(e)[:300]}

def main():
    p = argparse.ArgumentParser(prog="headers", description="HTTP security headers checker")
    p.add_argument("urls", nargs="+")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    for url in args.urls:
        if not url.startswith("http"):
            url = "https://" + url
        r = check_url(url)
        if args.json:
            print(json.dumps(r, indent=2))
            continue
        if "error" in r:
            print(f"❌ {url}: {r['error']}")
            continue
        print(f"\n🔒 {url}  —  Grade: {r['grade']} ({r['score_pct']}%)")
        if r["present"]:
            print("  ✅ Present:")
            for h in r["present"]:
                print(f"     {h['name']}: {h['value'][:80]}")
        if r["missing"]:
            print("  ❌ Missing:")
            for h in r["missing"]:
                sev = {"high": "🔴", "medium": "🟡", "low": "🟢"}[h["severity"]]
                print(f"     {sev} {h['name']} — {h['desc']}")
        if r["info_leak"]:
            print("  ⚠️  Info leakage:")
            for h in r["info_leak"]:
                print(f"     {h['name']}: {h['value']}")

if __name__ == "__main__":
    main()
