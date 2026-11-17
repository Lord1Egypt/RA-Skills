#!/usr/bin/env python3
"""Password breach exposure triage.

Checks passwords against the Have I Been Pwned Pwned Passwords
corpus using k-anonymity (only a 5-char SHA-1 prefix leaves the
machine), classifies what each relevant breach actually leaked,
and builds a severity-ranked rotation queue with blast-radius
math. Pure stdlib. State in scripts/data/.

Commands:
  check              interactive password check (hidden input)
  check --pw X ...   non-interactive check (mind shell history)
  assess             cross-reference with an account inventory,
                     emit ranked rotation queue
  catalog            offline catalog of landmark breaches
"""
import argparse
import getpass
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"
CACHE = DATA / "pwned_cache.json"
CATALOG = DATA / "breach_catalog.json"

API = "https://api.pwnedpasswords.com/range/{}"

# severity weights by leaked credential type
PLAINTEXT, FAST_HASH, STRONG_HASH, CONTACT_ONLY = 100, 80, 65, 10


def load_catalog():
    if CATALOG.exists():
        return json.loads(CATALOG.read_text())
    return []


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}


def save_cache(c):
    DATA.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(c, indent=2))


def pwned_count(password):
    """k-anonymity lookup. Returns (count or 0, network_ok)."""
    c = load_cache()
    h = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    if h in c:
        return c[h]["count"], True
    prefix, suffix = h[:5], h[5:]
    url = API.format(prefix)
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"Add-Padding": "true",
                              "User-Agent": "breach-exposure-triage"})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode()
            time.sleep(0.3)
            count = 0
            for line in body.splitlines():
                suf, cnt = line.split(":")
                if suf.strip() == suffix:
                    count = int(cnt)
                    break
            c[h] = {"count": count, "ts": int(time.time())}
            save_cache(c)
            return count, True
        except Exception:
            if attempt == 2:
                return 0, False
            time.sleep(1.5 * (attempt + 1))


def exposure_band(count):
    if count is None:
        return "UNKNOWN"
    if count == 0:
        return "CLEAN"
    if count < 100:
        return "NICHE"
    if count < 1000:
        return "KNOWN"
    if count < 100000:
        return "WORDLIST"
    return "UBIQUITOUS"


def cmd_check(a):
    passwords = list(a.pw) if a.pw else []
    if not passwords:
        print("Enter passwords to check (blank line to finish).")
        print("Only 5-char hash prefixes leave this machine.\n")
        while True:
            try:
                pw = getpass.getpass("password: ")
            except EOFError:
                break
            if not pw:
                break
            passwords.append(pw)
    if not passwords:
        sys.exit("no passwords to check")
    seen = {}
    results = []
    for pw in passwords:
        if pw in seen:
            results.append((pw, seen[pw][0], seen[pw][1]))
            continue
        count, ok = pwned_count(pw)
        seen[pw] = (count, ok)
        results.append((pw, count, ok))

    print(f"\n{'#':<3}{'EXPOSURE':<12}{'SEEN':>10}   VERDICT")
    print("-" * 72)
    any_net_fail = False
    for i, (pw, count, ok) in enumerate(results, 1):
        band = exposure_band(count)
        if not ok:
            any_net_fail = True
            note = "network unavailable - try again later"
        elif count == 0:
            note = "not in known corpus - keep, but check strength"
        elif count < 1000:
            note = "in corpus - rotate where reused"
        else:
            note = "in active wordlists - rotate EVERYWHERE + 2FA"
        print(f"{i:<3}{band:<12}{(count if count is not None else '?'):>10}   {note}")
        print(f"    len={len(pw)}  (value not stored; hash cached locally)")
    if any_net_fail:
        print("\nNOTE: some checks failed - results incomplete.")
    print("\nNext: run 'assess' with your account inventory to get "
          "a ranked rotation queue.")
    return results


def cmd_assess(a):
    inv_path = Path(a.inventory) if a.inventory else None
    inventory = []
    if inv_path and inv_path.exists():
        for ln in inv_path.read_text().splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split()
            acct = parts[0]
            base = parts[1] if len(parts) > 1 else "?"
            weight = float(parts[2]) if len(parts) > 2 else 1.0
            inventory.append({"account": acct, "base": base,
                              "weight": weight})
    catalog = load_catalog()
    if a.email:
        print(f"email in scope: {a.email}")
    print("\nRotation queue (severity x reuse x account weight)")
    print("=" * 78)

    rows = []
    for item in inventory:
        base = item["base"]
        count, ok = pwned_count(base) if base not in ("?", "") else (0, True)
        if not ok:
            print(f"  [net-fail] {item['account']}: cannot check now")
            continue
        sev = PLAINTEXT if count >= 1000 else (
            FAST_HASH if count > 0 else 0)
        reuse = sum(1 for x in inventory if x["base"] == base)
        priority = sev * (1 + reuse) * item["weight"]
        rows.append((priority, count, item, reuse))
    rows.sort(key=lambda r: r[0], reverse=True)
    if not rows:
        sys.exit("inventory empty - pass --inventory file with lines: "
                 "account base-nickname weight")
    for rank, (pri, count, item, reuse) in enumerate(rows, 1):
        band = exposure_band(count)
        why = (f"{band} ({count:,} corpus hits), reused on {reuse} "
               f"account(s), weight {item['weight']:.1f}")
        act = "ROTATE NOW + enable 2FA" if pri >= 200 else (
              "rotate this week" if pri >= 65 else "low-value rotation")
        print(f"{rank:>2}. {item['account']:<28} {act}")
        print(f"     {why}")
    print("=" * 78)
    print("Doctrine: email account first (it resets everything else),")
    print("then financial, then phone carrier (SIM-swap surface), then")
    print("the SOURCE account of the leak, then the rest.")


def cmd_catalog(_a=None):
    cat = load_catalog()
    if not cat:
        sys.exit("catalog missing")
    print(f"\n{'BREACH':<26}{'YEAR':>5}{'SCALE':>14}  LEAKED CLASS")
    print("-" * 78)
    for b in cat:
        print(f"{b['name'][:25]:<26}{b['year']:>5}{b['scale']:>14}"
              f"  {b['class']}")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.
                                 RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check passwords vs corpus")
    c.add_argument("--pw", action="append", default=[],
                   help="password to check (repeatable; prefer interactive)")
    c.set_defaults(func=cmd_check)
    s = sub.add_parser("assess", help="ranked rotation queue")
    s.add_argument("--email", default=None)
    s.add_argument("--inventory", default=None,
                   help="file: account base-nickname weight per line")
    s.set_defaults(func=cmd_assess)
    k = sub.add_parser("catalog", help="offline breach catalog")
    k.set_defaults(func=cmd_catalog)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
