#!/usr/bin/env python3
"""Identity breach first response — scope, contain, freeze, monitor, report.

Subcommands:
  scope    What leaked -> what it unlocks + reuse blast radius
  contain  Ordered first-minutes checklist (60/30/10 min modes)
  freeze   SSN-in-scope credit-freeze plan (3 bureaus, PINs, minors)
  monitor  90-day watch plan + monthly ritual
  report   FTC/police/dispute-letter generation when accounts were opened

Stdlib only. Offline. Defensive guidance only — never pay an extortionist.
"""
import argparse
import json
from datetime import date, timedelta

LEAK_FIELDS = {
    "email": ("Password resets for EVERY account tied to it", "email-first containment"),
    "password": ("Direct login where reused; credential stuffing everywhere else", "rotate siblings by importance"),
    "password-hash": ("Crackable — assume plaintext within days for weak ones", "same as password"),
    "phone": ("SIM-swap target + SMS-2FA interception", "port-out PIN + move off SMS 2FA"),
    "ssn": ("New accounts, tax refund theft, medical ID theft — for YEARS", "freeze all 3 bureaus + IRS IP PIN"),
    "dob": ("Verification answers + account-recovery knowledge", "fake security answers everywhere"),
    "security-answers": ("Old recovery questions fail as secrets", "replace with generated answers in manager"),
    "card": ("Charges within days; issuer re-issue", "card freeze + virtual numbers going forward"),
    "bank-account": ("ACH pulls/fraudulent transfers", "bank fraud line + account number change"),
    "address": ("Mail redirection, physical scams, address-verification data", "USPS Informed Delivery watch"),
    "id-scan": ("KYC bypass — fintech/exchange accounts in your name", "freeze + exchange KYC watch + FTC report"),
    "medical-id": ("Medical care in your name — records contamination", "request records from each provider"),
}

BUREAUS = [
    ("Equifax", "equifax.com/personal/credit-freeze", "1-800-685-1111"),
    ("TransUnion", "transunion.com/credit-freeze", "1-888-909-8872"),
    ("Experian", "experian.com/freeze/center", "1-888-397-3742"),
]

CONTAIN_STEPS = [
    ("0-10 min", "STOP using the suspect device for resets; grab a CLEAN phone/laptop", "resets done from an infected machine hand the new password over too"),
    ("0-10 min", "Primary EMAIL: new password -> REVOKE ALL SESSIONS -> check filters/forwarding -> verify recovery phone/email are yours", "email resets everything downstream; attackers leave silent forwarding rules"),
    ("10-20 min", "Password manager: rotate master password, re-pair its 2FA", "the manager is every other password"),
    ("10-20 min", "SIM-swap check: phone shows SOS/No Service? -> carrier FRAUD line (not the store), halt the port", "your SMS 2FA codes become his codes"),
    ("20-35 min", "Banking + cards: new passwords + transaction push alerts ON; fraud-claim any bad charges", "money moves fastest; claims have issuer windows"),
    ("20-35 min", "Re-enroll 2FA where seeds might have been seen; prefer app/passkey over SMS", "session tokens and seeds outlive passwords"),
    ("35-50 min", "Rotate REUSED sibling passwords by importance (shopping, social, gaming...)", "credential stuffing starts within hours"),
    ("35-50 min", "Carrier port-out PIN / Number Lock", "closes the door you just got hit through"),
    ("50-60 min", "Strip attacker-known recovery emails/phones from your OTHER accounts", "he owns the reset path to everything else otherwise"),
    ("60+ min", "Set a calendar: 30/60/90-day checks + freeze PINs stored in the manager", "the second wave shows up weeks later"),
]


def cmd_scope(a):
    leaked = [x.strip().lower() for x in a.leaked.split(",") if x.strip()]
    print("DAMAGE SCOPE — what the attacker actually holds")
    unknown = [f for f in leaked if f not in LEAK_FIELDS]
    for f in leaked:
        if f in LEAK_FIELDS:
            unlocks, move = LEAK_FIELDS[f]
            print(f"  {f:<18} -> {unlocks}")
            print(f"  {'':<18}    ACTION: {move}")
    if unknown:
        print(f"  ! unrecognized fields ignored: {', '.join(unknown)}")

    verdict = "CONTAIN NOW"
    sib = None
    if "ssn" in leaked or "id-scan" in leaked:
        verdict = "CONTAIN + FREEZE + LONG MONITORING (identity-theft class)"
    elif "password" in leaked or "password-hash" in leaked:
        verdict = "CONTAIN (credential class) + reuse sweep"
    elif leaked and all(f in ("email", "dob", "address") for f in leaked):
        verdict = "PHISHING RISK CLASS — expect targeted scams; contain email"

    print()
    print(f"VERDICT: {verdict}")
    if a.accounts and a.reuse:
        sib = int(a.accounts * a.reuse)
        print(f"REUSE MATH: {a.accounts} accounts x {int(a.reuse*100)}% reuse "
              f"= ~{sib} sibling accounts share that password —")
        print(f"  assume the stuffing list reaches them within days. Rotate by importance.")
    print()
    print("SESSION TRUTH: changing a password does NOT kick out a logged-in")
    print("attacker. 'Revoke sessions / log out devices' on every service, then")
    print("check email forwarding rules + connected-app grants.")
    return {"verdict": verdict, "sibling_accounts": sib if a.accounts and a.reuse else None}


def cmd_contain(a):
    steps = CONTAIN_STEPS
    if a.min == 30:
        steps = [s for s in steps if s[0] in ("0-10 min", "10-20 min", "20-35 min")][:6]
    print(f"CONTAINMENT — first {a.min} minutes, in ORDER (on a clean device)")
    for when, what, why in steps:
        print(f"[{when}] {what}")
        print(f"          WHY: {why}")
    print()
    print("RULES")
    print("  - Never click links in the breach email itself — type the company URL.")
    print("  - Claims windows: card issuers typically 60 days (statement), banks faster.")
    print("  - If phone went SOS -> treat as SIM swap: carrier fraud line FIRST.")
    return {"steps": len(steps)}


def cmd_freeze(a):
    if a.ssn != "yes":
        print("SSN not in scope -> FREEZE OPTIONAL. Recommended anyway if the")
        print("breach included DOB+address (synthetic-ID risk) or if you'll do")
        print("nothing else on this list. Locks are fine; freezes are the floor.")
        return {"freeze": "optional"}
    print("SSN IN SCOPE -> FREEZE ALL THREE BUREAUS (free, ~15 min total)")
    for name, url, phone in BUREAUS:
        print(f"  {name:<12} {url}  |  {phone}")
    print()
    print("MECHANICS")
    for line in (
        "  - Do all three; creditors pull different bureaus.",
        "  - Store the freeze PINs in the PASSWORD MANAGER — not email.",
        "  - Thaw 1 day when YOU apply for credit; lender names the bureau.",
        "  - Minors: phone/written request + guardianship proof — do it anyway",
        "    (clean child SSNs are prime targets).",
        "  - IRS IP PIN (irs.gov/ippin) — blocks e-file theft with your number.",
        "  - Already-opened accounts? -> `report` (FTC affidavit + disputes).",
    ):
        print(line)
    return {"bureaus": [b[0] for b in BUREAUS]}


def cmd_monitor(a):
    print("90-DAY WATCH PLAN")
    plan = [
        (date.today(), "Alerts ON: bank push per-transaction, all 3 bureau alerts, card-authorisation pings"),
        (date.today() + timedelta(days=1), "IRS IP PIN (if SSN); virtual card numbers for new online spending"),
        (date.today() + timedelta(days=7), "Pass 1: statements line-by-line; unknown ACH/charges"),
        (date.today() + timedelta(days=30), "Check 1: bureau dashboards for new accounts; any mail for accounts you never opened"),
        (date.today() + timedelta(days=60), "Check 2: repeat; + email recovery settings audit on critical accounts"),
        (date.today() + timedelta(days=90), "Check 3: repeat; decide freeze keep/thaw; log lessons"),
    ]
    for when, what in plan:
        print(f"  {when.isoformat()}  {what}")
    print()
    print("ESCALATE TO `report` IF: new account on file / collections letter /")
    print("tax refund hijack / medical bill in your name.")
    return {"checks": len(plan)}


def cmd_report(a):
    print("IDENTITY-THEFT REPORT PACK")
    print()
    print("1) FTC report (the affidavit banks/bureaus actually want):")
    print("   identitytheft.gov -> 'Get started' -> walk the wizard ->")
    print("   SAVE the report NUMBER — it goes on every dispute letter.")
    if a.ftc_number:
        print(f"   Using FTC report number: {a.ftc_number}")
    print("2) Police report (banks may ask for the number):")
    print("   non-emergency line / online portal -> category 'identity theft'")
    print("   bring: FTC report, your ID, the fraudulent account letters")
    print("3) Bureau dispute letter per fraudulent item (FCRA 605B blocking):")
    letter = f"""{date.today().isoformat()}

{a.bureau or '[Bureau name]'} — Fraud/Disputes Department
RE: Blocking of identity-theft items — FTC report #{a.ftc_number or '[number]'}

Under FCRA section 605B I request that the following information result-
ing from identity theft be blocked from my credit report within 4
business days:

  {a.items or '[creditor / account number / date opened]'}

Enclosed: FTC Identity Theft Report, proof of my identity, police
report #{a.police or '[if filed]'}.

Please confirm the block in writing and notify the furnisher.

Sincerely,
{a.name or '[your name]'}
"""
    print()
    print(letter)
    print("Send certified mail, return receipt. Keep copies of everything.")
    return {"letter_generated": True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("scope")
    sp.add_argument("--leaked", required=True,
                    help="comma list: password,email,phone,ssn,dob,card,...")
    sp.add_argument("--accounts", type=int, default=None, help="total accounts you hold")
    sp.add_argument("--reuse", type=float, default=None, help="reuse fraction 0-1")
    sp.set_defaults(fn=cmd_scope)

    sp = sub.add_parser("contain")
    sp.add_argument("--min", type=int, default=60, choices=[10, 30, 60])
    sp.set_defaults(fn=cmd_contain)

    sp = sub.add_parser("freeze")
    sp.add_argument("--ssn", default="yes", choices=["yes", "no"])
    sp.set_defaults(fn=cmd_freeze)

    sp = sub.add_parser("monitor")
    sp.set_defaults(fn=cmd_monitor)

    sp = sub.add_parser("report")
    sp.add_argument("--ftc-number", default=None)
    sp.add_argument("--police", default=None)
    sp.add_argument("--bureau", default=None)
    sp.add_argument("--items", default=None)
    sp.add_argument("--name", default=None)
    sp.set_defaults(fn=cmd_report)

    a = p.parse_args()
    out = a.fn(a)
    if a.json:
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
