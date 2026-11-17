#!/usr/bin/env python3
"""Password manager migration planner — plans and audits, never secrets.

Subcommands:
  plan      Best route + lost-field list + ordered steps for a hop
  worksheet Field-mapping CSV + dedupe precedence rules
  totp      TOTP loss assessment + re-enrollment protocol for a hop
  audit     Count-based post-migration verification

Works ONLY from metadata/counts. Zero network, zero secret handling.
"""
import argparse
import csv
import io
import json

MANAGERS = ["bitwarden", "1password", "keepass", "chrome", "proton", "safari"]

# hop -> (best_route, survives, lost, notes)
ROUTES = {
    ("bitwarden", "1password"): (
        "1Password native importer (Settings > Import > Bitwarden)",
        ["logins", "notes", "cards", "identities", "TOTP seeds"],
        ["folders -> tags (approximate mapping)", "attachments (manual re-add)",
         "collection sharing (must re-share)"],
        "Import into a fresh vault first, verify, then merge into your real one."),
    ("bitwarden", "keepass"): (
        "KeePassXC: Import > Bitwarden JSON (or via CSV with field mapping)",
        ["logins", "notes", "TOTP (otp field)", "folders -> groups"],
        ["attachments", "custom fields beyond notes (partial)", "send items"],
        "KeePassXC reads Bitwarden encrypted-JSON? No — use unencrypted JSON export, offline machine."),
    ("1password", "bitwarden"): (
        "Bitwarden native importer (Tools > Import data > 1Password)",
        ["logins", "secure notes", "TOTP", "identities (partial)"],
        ["tags", "vault structure (multi-vault collapses)", "attachments/documents",
         "watchtower markers"],
        "Export as 1PIUX or unencrypted .1pux — count documents before/after."),
    ("keepass", "bitwarden"): (
        "Bitwarden native importer (Tools > Import > KeePass 2 XML)",
        ["logins", "notes", "TOTP seeds (otp field)", "groups -> folders"],
        ["icons", "entry history", "auto-type associations", "custom date fields"],
        "Export KeePass 2.x database as XML (not CSV) to keep TOTP + groups."),
    ("chrome", "bitwarden"): (
        "Bitwarden native Chrome importer (via chrome://settings export CSV)",
        ["logins (URL, user, pass)"],
        ["TOTP", "folders/labels", "passkeys", "payment methods",
         "passwords saved AFTER the export"],
        "CSV lives plaintext on disk — secure-delete after import."),
    ("bitwarden", "chrome"): (
        "CSV export/import (chrome://settings > Import)",
        ["logins (URL, user, pass)"],
        ["TOTP", "folders", "notes attachments", "cards", "identities"],
        "Chrome accepts logins only — run totp() first."),
    ("proton", "bitwarden"): (
        "Bitwarden native Proton importer (Proton Pass export JSON/CSV)",
        ["logins", "notes", "TOTP"],
        ["hide-my-email aliases (verify forwarding still routes)",
         "custom fields (partial)"],
        "Aliases keep working only if the forwarding stays active — test one."),
    ("bitwarden", "proton"): (
        "Proton Pass importer (Settings > Import > Bitwarden)",
        ["logins", "notes", "TOTP"],
        ["folders -> vaults (one-level only)", "attachments", "sends"],
        "Proton maps folders to vaults — plan your vault layout first."),
    ("safari", "bitwarden"): (
        "Bitwarden Safari/ICloud importer (via export from Safari settings)",
        ["logins"],
        ["TOTP (iCloud keychain OTPs don't export)", "secure notes (export separately)",
         "passkeys"],
        "Apple hides exports on iOS; use the Mac to export."),
    ("keepass", "1password"): (
        "1Password native KeePass importer",
        ["logins", "notes", "TOTP"],
        ["groups -> tags (approx)", "icons", "history"],
        "Test with a copy of the database — importer quirks with old KeePass 1 entries."),
    ("chrome", "1password"): (
        "1Password native Chrome importer",
        ["logins"],
        ["TOTP", "passkeys", "payment methods"],
        "Same CSV caveats — plaintext on disk during the hop."),
}

CSV_HOP_LOSS = {
    "totp": "ALL TOTP seeds are dropped by every CSV hop, without error.",
    "folders": "Folder/group structure is dropped (some targets rebuild from URLs).",
    "attachments": "Attachments never ride CSV.",
    "cards": "Most CSV hops skip cards/identities entirely.",
    "dates": "Modified-dates become the export date — dedupe by date breaks.",
}


def plan_hop(src, dst, merge=False):
    if merge or src == dst:
        return {
            "mode": "MERGE (same manager)",
            "route": "Import the secondary vault's export into the primary (or an org), then dedupe inside",
            "survives": ["everything the format supports"],
            "lost": ["duplicate identity — see precedence rules"],
            "steps": [
                "1. Export BOTH vaults in the richest format available (JSON/XML, never CSV).",
                "2. Import the secondary into a SEPARATE folder/vault in the primary.",
                "3. Run the target's duplicate detector INSIDE the tool.",
                "4. Apply precedence: newer modified-date wins; conflicts -> manual review list.",
                "5. Audit counts: pre1 + pre2 - dedupes = post.",
                "6. Keep secondary vault read-only 30 days.",
            ],
        }
    key = (src, dst)
    if key not in ROUTES:
        alt = [k for k in ROUTES if k[0] == src or k[1] == dst]
        return {"error": f"no direct route data for {src} -> {dst}",
                "known_routes": [f"{s}->{d}" for s, d in alt]}
    route, survives, lost, note = ROUTES[key]
    steps = [
        f"1. PRE-COUNT: note item counts per type in {src} (logins/notes/cards/TOTP/attachments) — this is your audit baseline.",
        f"2. EXPORT from {src}: {route}.",
        "3. SECURITY: exports are PLAINTEXT. Work offline, out of cloud-sync folders; secure-delete after.",
        f"4. IMPORT into {dst} into a fresh/import vault first (not your main).",
        "5. SPOT-CHECK: 5 random logins + 1 bank + 1 TOTP entry — fields in right places?",
        "6. COUNT-AUDIT: run `audit` with pre/post counts; explain every delta.",
        "7. TOTP: run `totp` — re-enroll what the hop drops BEFORE deleting anything.",
        "8. ATTACHMENTS: manual re-add, count against baseline.",
        "9. CUTOVER: set old vault read-only 30 days; browser extensions switched; calendar reminder to delete.",
    ]
    return {"mode": f"{src} -> {dst}", "route": route, "survives": survives,
            "lost": lost, "quirk": note, "steps": steps,
            "lost_warning": f"These do NOT survive and will NOT error: {', '.join(lost)}"}


def cmd_plan_args(a):
    return plan_hop(a.src, a.dst, merge=a.merge)


FIELD_MAP = {
    ("keepass", "bitwarden"): [
        ("Title", "Name"),
        ("UserName", "Username"),
        ("Password", "Password"),
        ("URL", "URI 1 (login URI)"),
        ("Notes", "Notes"),
        ("TOTP Seed", "Authenticator key (TOTP)"),
        ("Group", "Folder"),
        ("Tags", "— (no equivalent; append to notes)"),
    ],
    ("chrome", "bitwarden"): [
        ("name", "Name"),
        ("url", "URI"),
        ("username", "Username"),
        ("password", "Password"),
        ("—", "Folder (manual)"),
        ("—", "TOTP (LOST — re-enroll)"),
    ],
    ("bitwarden", "csv-generic"): [
        ("name", "name"),
        ("login_uri", "url"),
        ("login_username", "username"),
        ("login_password", "password"),
        ("login_totp", "(dropped by CSV)"),
        ("folder", "(dropped by CSV)"),
        ("notes", "note (length limits on some targets)"),
    ],
}


def cmd_worksheet(a):
    key = (a.src, a.dst)
    rows = FIELD_MAP.get(key) or [
        ("(source field)", "(target field)"),
        ("Name/Title", "Name"),
        ("Username", "Username"),
        ("Password", "Password"),
        ("URL", "URI"),
        ("Notes", "Notes"),
        ("TOTP", "Authenticator key"),
        ("Folder/Group", "Folder/Tag"),
    ]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow([f"{key[0]} field", f"{key[1]} field", "verified?"])
    for r in rows:
        w.writerow(list(r) + [""])
    return {
        "worksheet_csv": buf.getvalue(),
        "dedupe_precedence": [
            "1. Exact URI + username match -> keep NEWER modified-date entry.",
            "2. Same username, different URI (http/https, www) -> normalize URI, then rule 1.",
            "3. Different username, same site -> KEEP BOTH (could be role accounts).",
            "4. Empty/passwordless entry vs full entry -> keep full.",
            "5. ANY conflict you can't decide in 5 seconds -> flag 'review', never auto-pick.",
        ],
        "rules": [
            "Never pre-dedupe before import — import everything, dedupe in-target.",
            "After CSV hops, ignore modified-dates entirely (they're export dates).",
            "Logins with TOTP in source and no TOTP in target = re-enroll list item.",
        ],
    }


def cmd_totp(a):
    if a.via == "csv":
        lost = list(CSV_HOP_LOSS.values())
        return {
            "verdict": "FATAL for TOTP via CSV: every seed is dropped silently.",
            "what_happens": lost,
            "protocol": [
                "1. BEFORE export: list entries with TOTP in the source (the manager's TOTP filter/view).",
                "2. For each: confirm you can log in WITHOUT the TOTP (password + backup codes).",
                "3. If yes: plan re-enrollment post-migration (scan new QR into the new manager).",
                "4. If no: enroll a SECOND method first (SMS/email backup), then migrate.",
                "5. Store backup/recovery codes as secure notes NOW if not already.",
                "6. Only after every TOTP entry is re-enrolled in the target: delete the source.",
            ],
            "blurb": "TOTP seeds are one-shot: if the hop drops them, only a working login + re-enrollment recovers them.",
        }
    return {
        "verdict": "Native/JSON routes usually keep TOTP — but VERIFY per entry, importers do drop seeds silently on format quirks.",
        "protocol": [
            "1. Count TOTP entries in source (filter/view).",
            "2. Post-import, count TOTP entries in target.",
            "3. Any delta = the re-enrollment list. Handle before cutover.",
            "4. Keep recovery codes for those sites as secure notes regardless.",
        ],
    }


def cmd_audit(a):
    deltas = []
    ok = True
    for kind in ("logins", "notes", "cards"):
        pre = getattr(a, f"pre_{kind}")
        post = getattr(a, f"post_{kind}")
        if pre is None or post is None:
            continue
        d = post - pre
        if d < 0:
            ok = False
            deltas.append(f"{kind}: LOST {-d} items (pre {pre} -> post {post}) — importer dropped entries, find them")
        elif d == 0:
            deltas.append(f"{kind}: exact match ({pre})")
        else:
            deltas.append(f"{kind}: +{d} (pre {pre} -> post {post}) — expected only if you merged/added")
    out = {"counts": deltas, "duplicates_reported": a.duplicates,
           "weak_left": a.weak_left}
    if not ok:
        out["verdict"] = "FAIL — item losses found. Do NOT delete the old vault."
        out["recovery"] = [
            "Diff the exports: sort both by URI+username, find the missing.",
            "Common silent drops: entries with no name, non-ASCII names, oversized notes, attachments.",
            "Re-export those entries individually and re-import.",
        ]
    else:
        out["verdict"] = "PASS on counts — proceed to TOTP + attachment verification."
    if a.duplicates:
        out["dedupe_next"] = (f"{a.duplicates} duplicates reported: apply precedence rules "
                              "(see worksheet), review conflicts manually.")
    if a.weak_left:
        out["hygiene"] = (f"{a.weak_left} weak/reused passwords remain: schedule "
                          "rotation — the manager's security report ranks them; start with "
                          "email, bank, and anything financial.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("plan")
    sp.add_argument("--src", required=True, choices=MANAGERS)
    sp.add_argument("--dst", required=True, choices=MANAGERS)
    sp.add_argument("--merge", action="store_true", help="same-manager vault merge")
    sp.set_defaults(fn=cmd_plan_args)

    sp = sub.add_parser("worksheet")
    sp.add_argument("--src", required=True, choices=MANAGERS)
    sp.add_argument("--dst", required=True, choices=MANAGERS + ["csv-generic"])
    sp.set_defaults(fn=cmd_worksheet)

    sp = sub.add_parser("totp")
    sp.add_argument("--via", default="native", choices=["native", "csv"])
    sp.set_defaults(fn=cmd_totp)

    sp = sub.add_parser("audit")
    sp.add_argument("--pre-logins", type=int)
    sp.add_argument("--post-logins", type=int)
    sp.add_argument("--pre-notes", type=int)
    sp.add_argument("--post-notes", type=int)
    sp.add_argument("--pre-cards", type=int)
    sp.add_argument("--post-cards", type=int)
    sp.add_argument("--duplicates", type=int, default=0)
    sp.add_argument("--weak-left", type=int, default=0)
    sp.set_defaults(fn=cmd_audit)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
