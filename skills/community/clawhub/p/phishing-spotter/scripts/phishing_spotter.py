#!/usr/bin/env python3
"""Phishing Spotter — textual phishing/smishing/vishing analysis.

Dissects URLs (homograph tricks, subdomain spoofs, shorteners, punycode),
scores 25+ social-engineering pressure patterns, checks structural tells,
and explains every signal in plain language. Never fetches anything.

Usage:
    phishing_spotter.py analyze <file> [--json]
    phishing_spotter.py url "<url>"
    phishing_spotter.py list-patterns
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from urllib.parse import unquote, urlparse

# --------------------------------------------------------------------------
# Known reference data (offline)
# --------------------------------------------------------------------------

SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly",
    "adobe.ly", "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy", "lnkd.in",
    "tiny.cc", "bit.do", "v.gd", "s.id", "shorte.st", "bl.ink", "tinyurl.link",
}

BRANDS = [
    "paypal", "apple", "icloud", "microsoft", "office", "outlook", "google",
    "gmail", "amazon", "netflix", "facebook", "instagram", "whatsapp",
    "linkedin", "twitter", "x.com", "chase", "wellsfargo", "citibank",
    "bankofamerica", "hsbc", "santander", "sberbank", "vtb", "alfabank",
    "tinkoff", "raiffeisen", "dhl", "fedex", "ups", "usps", "royalmail",
    "Internal Revenue Service", "irs", "hmrc", "steam", "roblox", "discord",
    "telegram", "revolut", "wise", "coinbase", "binance", "metamask",
]

CRED_BAIT = [
    "login", "signin", "sign-in", "verify", "verification", "confirm",
    "account", "secure", "update", "wallet", "password", "billing",
    "unlock", "suspend", "recovery", "authenticate", "session",
]

RISKY_TLDS = {"tk", "ml", "ga", "cf", "gq", "xyz", "top", "buzz", "click",
              "link", "work", "bar", "rest", "fit", "cam", "surf", "monster",
              "quest", "cyou", "sbs"}

RISKY_ATTACH = {".exe", ".scr", ".js", ".vbs", ".hta", ".jar", ".cmd",
                ".bat", ".msi", ".iso", ".img", ".zip", ".rar", ".7z",
                ".docm", ".xlsm", ".pptm"}

# --------------------------------------------------------------------------
# URL forensics
# --------------------------------------------------------------------------


def registrable_domain(host: str) -> str:
    """Crude registrable domain: last two labels (works for co.uk poorly,
    acceptable for triage)."""
    if not host:
        return ""
    labels = host.split(".")
    if len(labels) >= 3 and labels[-2] in ("co", "com", "org", "net", "gov", "ac", "edu"):
        return ".".join(labels[-3:])
    return ".".join(labels[-2:]) if len(labels) >= 2 else host


def mixed_script(host: str) -> list[str]:
    """Return characters in the host that come from unexpected scripts."""
    suspicious = []
    for ch in host:
        if ch.isascii():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if any(s in name for s in ("CYRILLIC", "GREEK", "ARMENIAN", "HEBREW", "ARABIC")):
            suspicious.append(ch)
    return suspicious


def analyze_url(url: str) -> dict:
    """Character-level forensics on one URL. Never fetches."""
    f = {"url": url, "signals": []}

    # unquote %xx tricks first
    decoded = unquote(url)

    try:
        p = urlparse(decoded if "://" in decoded else f"http://{decoded}")
    except ValueError:
        f["signals"].append({"code": "unparseable", "weight": 8,
                             "note": "URL failed to parse — often deliberate obfuscation"})
        return f

    host = (p.hostname or "").lower()
    f["host"] = host
    f["registrable"] = registrable_domain(host)
    f["path"] = p.path or "/"

    def sig(code, weight, note):
        f["signals"].append({"code": code, "weight": weight, "note": note})

    if not host:
        sig("no_host", 6, "No host in URL")
        return f

    # 1. punycode
    if "xn--" in host:
        sig("punycode", 22, "Punycode (xn--) host encodes non-ASCII characters — "
            "the classic homograph attack (e.g., а fake 'аpple.com' with a Cyrillic а).")

    # 2. mixed-script homoglyphs in a non-punycode host (raw unicode)
    weird = mixed_script(host)
    if weird:
        sig("homograph", 25, f"Host contains non-Latin characters that look Latin: "
            f"{''.join(weird)!r} — homograph spoofing.")

    # 3. brand in subdomain: brand.com.evil.io / brand.com.evil.io
    reg = f["registrable"]
    for b in BRANDS:
        bl = b.lower().split()[0]
        if not bl or bl == reg or reg.endswith(f".{bl}.com"):
            continue
        # brand label present but NOT the registrable domain
        if re.search(rf"(?:^|[.-]){re.escape(bl)}(?:\.com)?(?:$|[.-])", host) and bl not in reg.split("."):
            sig("brand_subdomain", 25, f"'{b}' appears in the host but the actual site is "
                f"'{reg}'. Read domains right-to-left: only the last labels matter. "
                f"Subdomain spoof.")
            break

    # 4. IP host
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        sig("ip_host", 15, "Host is a raw IP address — no organization runs a login "
            "page on a bare IP.")

    # 5. shortener
    if reg in SHORTENERS:
        sig("shortener", 10, "URL shortener hides the destination. Expand safely "
            "(e.g., curl -I without following) before trusting — or just don't trust it.")

    # 6. '@' trickery: http://paypal.com@evil.io
    if "@" in (p.netloc or ""):
        sig("at_trick", 20, "'@' in the URL authority: everything before @ is a decoy "
            "username; the real host is after it.")

    # 7. credential-bait path
    path_l = (p.path or "").lower()
    bait_hits = [c for c in CRED_BAIT if re.search(rf"/{c}(/|$|\b)", path_l)]
    if bait_hits:
        sig("cred_bait", 12, f"Path contains credential-bait words: "
            f"{', '.join(bait_hits[:3])} — typical of credential harvesters.")

    # 8. risky TLD
    tld = host.rsplit(".", 1)[-1] if "." in host else ""
    if tld in RISKY_TLDS:
        sig("risky_tld", 8, f".{tld} is a cheap/free TLD heavily abused for phishing "
            f"campaigns.")

    # 9. encoded host (hex or %xx in netloc)
    if re.search(r"%[0-9a-f]{2}", p.netloc or "", re.I):
        sig("encoded_host", 15, "Percent-encoded characters in the host — obfuscation.")

    # 10. brand name in path but not host: evil.io/paypal/login
    for b in BRANDS[:20]:
        bl = b.lower().split()[0]
        if bl in path_l and bl not in host:
            sig("brand_in_path", 10, f"'{b}' appears in the PATH, not the domain — "
                f"the page lives on unrelated infrastructure.")
            break

    # 11. http (not https) on something pretending to be sensitive
    if p.scheme == "http" and any(c in path_l for c in ("login", "verify", "account", "password")):
        sig("plain_http_cred", 15, "Plain http:// for a login-shaped URL — no transport "
            "security at all.")

    return f


# --------------------------------------------------------------------------
# Pressure patterns
# --------------------------------------------------------------------------

PATTERNS = [
    ("deadline", 15, r"\b(within|in|before)\s+(24|48|72|12|48 hours|\d+\s*(hours?|days?|minutes?))\b",
     "Artificial deadline. Real institutions give notice, not countdowns — urgency exists to stop you thinking."),
    ("account_loss", 12, r"\b(account|cards?)\s+(will\s+be\s+)?(permanently\s+)?(suspended|closed|terminated|blocked|locked|restricted|deactivated)\b",
     "Threat of account loss — the #1 phishing motivator. Banks don't suspend accounts by email."),
    ("legal_action", 12, r"\b(legal (action|proceedings)|lawsuit|court|prosecut|warrant|arrest|final notice|enforcement)\b",
     "Legal-threat pressure. Real legal process arrives by post/court, not email ultimatums."),
    ("authority", 8, r"\b(ceo|cfo|director|president|chief|head of|hr department|support team|security team|system administrator)\b.{0,80}\b(requests?|asks?|needs?|requires?|immediately|urgent)\b",
     "Authority pressure — impersonating a boss/official to bypass your judgment."),
    ("curiosity", 8, r"\b(you have (1|one|a)|new message|you won|winner|unclaimed|awaiting you|exclusive (offer|deal)|you.{0,30}selected)\b",
     "Curiosity/reward bait — dangling something to get the click before thought."),
    ("lottery", 15, r"\b(lottery|prize|inheritance|beneficiary|next of kin|unclaimed funds|donation)\b",
     "Advance-fee lure (lottery/inheritance). If you never entered, you never won."),
    ("gift_card", 15, r"\b(gift ?cards?|apple ?cards?|steam ?cards?|google play|itunes card)\b",
     "Gift cards as payment — no legitimate business bills in gift cards. Ever."),
    ("crypto_pay", 12, r"\b(bitcoin|btc|ethereum|eth|usdt|crypto wallet|wallet address)\b",
     "Crypto payment rail — irreversible and untraceable; standard for scams."),
    ("wire", 10, r"\b(wire transfer|bank transfer|send.{0,20}(funds|money)|zelle|western union|moneygram)\b",
     "Wire/transfer-instruction pressure — irreversible payment rails."),
    ("verify_now", 12, r"\b(verify|confirm|validate|update|review)\s+(your|the)?\s*(account|identity|payment|billing|password|details?|information)\b",
     "Verification demand — manufactures a reason to harvest credentials."),
    ("click_here", 6, r"\b(click here|click the (link|button)|tap here|follow this link|log ?in.{0,30}(here|below))\b",
     "Click-here nudge instead of telling you what/where. Legit mail names destinations."),
    ("mismatch_generic_greeting", 6, r"^(dear (customer|user|sir|madam|account holder|client)|attention|greetings)\b",
     "Generic greeting — a real institution knows your name."),
    ("secrecy", 12, r"\b(confidential|do not (tell|inform|discuss|share)|keep this (private|between us)|discreet)\b",
     "Secrecy request — isolating you from people who'd spot the scam."),
    ("unusual_sender_domain", 10, r"@(gmail|hotmail|outlook|yahoo|yandex|mail|proton|icloud)\.",
     "Corporate/business claims from a free-mail domain."),
    ("attachment_urgent", 10, r"\b(see (attached|invoice|report)|open the (attachment|file)|download.{0,20}(invoice|report|document))\b",
     "Pressure to open an attachment — the malware delivery vector."),
    ("fear_data_breach", 12, r"\b(unusual (activity|sign-?in)|suspicious (activity|login)|security alert|unauthorized access|compromised)\b",
     "Data-breach fear — alarming you into 'fixing' via their link."),
    ("too_good", 12, r"\b(\d{2,}% (off|discount)|free (money|gift|iphone|prize)|guaranteed (returns?|income|profit)|risk-?free)\b",
     "Too-good-to-be-true economics. It is."),
    ("payment_rush", 10, r"\b(invoice|payment|balance|due|overdue|outstanding).{0,60}\b(immediately|right away|at once|today|now)\b",
     "Payment urgency pairing — an amount + a clock is classic invoice fraud."),
    ("missed_delivery", 10, r"\b(missed (delivery|shipment|package)|parcel (is )?(on hold|waiting|pending)|customs fee|redelivery)\b",
     "Delivery-fee lure — extremely common smishing template."),
    ("tax_refund", 12, r"\b(tax (refund|return|rebate)|irs|hmrc|refund (of|is) \d|stimulus)\b",
     "Tax-refund bait — agencies don't email refunds with links."),
    ("romance", 12, r"\b(my (love|dear|darling)|i love you|traveling abroad|stuck in|customs|hospital bills|need your help)\b",
     "Romance-scam phrasing — affection plus a crisis plus a payment."),
    ("tech_support", 10, r"\b(your (computer|device|pc) (is|has)|virus detected|malware|call (this|our) (number|support))\b",
     "Fake tech-support scare — the goal is remote access or 'refund' access to your bank."),
    ("biz_email_compromise", 12, r"\b(updated (bank )?details|new (bank )?account|changed (our|my) (bank|payment|invoice) (details|info|account)|urgent payment)\b",
     "BEC pattern — 'our bank details changed' invoice redirection."),
    ("otp_request", 15, r"\b(send|share|provide|read (out|back)).{0,40}\b(code|otp|pin|passcode|verification code|2fa)\b",
     "Asking for YOUR one-time code — the final step of account takeover. No one legitimate will ever ask."),
    ("callback_pressure", 8, r"\b(call|phone|speak).{0,30}\b(immediately|right now|straight away|before.{0,20}end of day)\b",
     "Callback pressure — vishing escalation path."),
]

# --------------------------------------------------------------------------
# Message analysis
# --------------------------------------------------------------------------


def parse_eml(text: str):
    """Split headers from body (loose .eml handling)."""
    if "\n\n" in text:
        head, body = text.split("\n\n", 1)
    elif "\r\n\r\n" in text:
        head, body = text.split("\r\n\r\n", 1)
    else:
        return {}, text
    headers = {}
    for line in head.splitlines():
        m = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if m:
            headers[m.group(1).lower()] = m.group(2).strip()
    return headers, body


URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"')\]]+", re.I)


def analyze_message(text: str) -> dict:
    headers, body = parse_eml(text)
    full = text

    signals = []

    def add(code, weight, note, evidence=""):
        signals.append({"code": code, "weight": weight, "note": note,
                        "evidence": evidence[:200]})

    # --- URL forensics
    urls = []
    seen = set()
    for m in URL_RE.finditer(full):
        u = m.group(0).rstrip(".,;:!?")
        if u not in seen:
            seen.add(u)
            urls.append(analyze_url(u))
    for uf in urls:
        for s in uf["signals"]:
            add(s["code"], s["weight"], s["note"], uf["url"])

    # --- pressure patterns
    for code, weight, pat, note in PATTERNS:
        m = re.search(pat, full, re.I | re.MULTILINE)
        if m:
            add(code, weight, note, m.group(0))

    # --- structural tells
    from_header = headers.get("from", "")
    reply_to = headers.get("reply-to", "")
    if from_header and reply_to:
        fd = re.search(r"@([\w.-]+)", from_header)
        rd = re.search(r"@([\w.-]+)", reply_to)
        if fd and rd and registrable_domain(fd.group(1)) != registrable_domain(rd.group(1)):
            add("reply_to_divergence", 12,
                "Reply-To points to a DIFFERENT domain than From — replies go to the attacker.",
                f"From: {from_header} / Reply-To: {reply_to}")

    display = re.match(r'^"?"?([^"<]{2,40})"?<?', from_header)
    if display and "@" not in display.group(1):
        dn = display.group(1).strip().lower()
        for b in BRANDS:
            bl = b.lower().split()[0]
            if bl in dn:
                fd = re.search(r"@([\w.-]+)", from_header)
                if fd and bl not in fd.group(1).lower():
                    add("display_name_mismatch", 12,
                        f"Display name claims '{display.group(1).strip()}' but the sending "
                        f"domain is {fd.group(1)} — impersonation via display name.",
                        from_header)
                break

    # attachments
    atts = re.findall(r"([\w.-]+\.(?:exe|scr|js|vbs|hta|jar|cmd|bat|msi|iso|img|zip|rar|7z|docm|xlsm|pptm|pdf))", full, re.I)
    risky = [a for a in atts if a.lower().endswith(tuple(RISKY_ATTACH))]
    if risky:
        add("risky_attachment", 15,
            f"Risky attachment type(s): {', '.join(risky[:3])} — malware delivery.", ", ".join(risky[:3]))

    # personalization absence
    if re.search(r"\b(dear (customer|user|sir|madam|client|account holder))\b", full, re.I):
        pass  # already caught by mismatch_generic_greeting

    score = min(sum(s["weight"] for s in signals), 100)
    band = ("ALMOST CERTAINLY PHISHING" if score >= 75 else
            "LIKELY PHISHING" if score >= 50 else
            "SUSPICIOUS — verify independently" if score >= 25 else
            "LOW RISK (still verify anything asking for credentials)")

    return {
        "score": score,
        "band": band,
        "signal_count": len(signals),
        "signals": sorted(signals, key=lambda s: -s["weight"]),
        "urls": [{k: v for k, v in u.items() if k != "signals"} for u in urls],
    }


VERIFY_STEPS = """BEFORE YOU ACT — verify independently:
  1. Open the institution's app/site directly (type it yourself). Any real
     "suspicious activity" or "action required" notice will be visible there too.
  2. If unsure, call the number ON YOUR CARD / official statement — never one
     from the message.
  3. Report: forward to phishing@<real-brand-domain>, reportphishing@apwg.org;
     then delete."""


def render(report: dict) -> str:
    lines = []
    lines.append(f"RISK SCORE: {report['score']}/100 — {report['band']}")
    lines.append(f"Based on {report['signal_count']} signals. "
                 "Do not click, do not reply, do not open attachments.\n")
    lines.append("TOP SIGNALS:")
    for s in report["signals"][:10]:
        lines.append(f"[+{s['weight']}] {s['code'].upper()}")
        if s["evidence"]:
            lines.append(f"  Evidence: \"{s['evidence']}\"")
        lines.append(f"  {s['note']}")
    if report["urls"]:
        lines.append("\nURL ANALYSIS:")
        for i, u in enumerate(report["urls"], 1):
            lines.append(f"  {i}. {u['url'][:100]}")
            lines.append(f"     host={u.get('host','?')}  registrable={u.get('registrable','?')}")
    lines.append("\n" + VERIFY_STEPS)
    lines.append("\nSIGNALS TO MEMORIZE FROM THIS MESSAGE:")
    for i, s in enumerate(report["signals"][:3], 1):
        lines.append(f"  {i}. {s['code'].replace('_',' ')} — {s['note'][:120]}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Textual phishing analysis (never fetches)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("file")
    a.add_argument("--json", action="store_true")
    u = sub.add_parser("url")
    u.add_argument("target")
    sub.add_parser("list-patterns")
    args = ap.parse_args()

    if args.cmd == "list-patterns":
        for code, weight, pat, note in PATTERNS:
            print(f"[{weight:3}] {code:24} {note[:90]}")
        return 0

    if args.cmd == "url":
        f = analyze_url(args.target)
        print(f"URL: {f['url']}")
        print(f"host={f.get('host')}  registrable={f.get('registrable')}")
        if f["signals"]:
            print("SIGNALS:")
            for s in f["signals"]:
                print(f"  [+{s['weight']}] {s['code']}: {s['note']}")
        else:
            print("no URL-level signals (message context still matters)")
        return 0

    text = open(args.file, encoding="utf-8", errors="replace").read()
    if len(text.strip()) < 20:
        print("error: message too short", file=sys.stderr)
        return 1
    report = analyze_message(text)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
