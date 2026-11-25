#!/usr/bin/env python3
"""House-Sitter Handoff — briefing packet generator + readiness audit.

Input: home registry JSON (see sample_home.json).
Output: HANDOFF.md (full briefing) + EMERGENCY_CARD.md (fridge one-pager).

--audit-only prints gaps and exits 1 on CRITICAL findings.
stdlib only.
"""
import argparse
import json
import sys
import os

POISON_LINES = {
    "US": "Poison Control 1-800-222-1222",
    "EU": "112 (ask for poison centre)",
    "UK": "NHS 111 (poisons)",
}


def audit(reg, winter):
    crit, warn = [], []
    h = reg.get("household", {})

    pets = reg.get("pets", [])
    for p in pets:
        vet = p.get("vet") or {}
        if not vet.get("phone"):
            crit.append(f"pet '{p.get('name','?')}' has no vet phone")
        if not p.get("feeding"):
            crit.append(f"pet '{p.get('name','?')}' has no feeding instructions")

    contacts = reg.get("contacts", [])
    if not any(c.get("phone") for c in contacts):
        crit.append("no contact with a phone number at all")
    elif not contacts:
        crit.append("contacts list is empty")

    shutoffs = reg.get("shutoffs", {})
    if winter and not shutoffs.get("water_main"):
        crit.append("winter packet without water-main shutoff location "
                    "(burst-pipe risk)")
    if winter:
        esc = json.dumps(reg.get("escalation", []))
        if "heating" not in esc.lower():
            crit.append("winter packet without a no-heating escalation step")

    alarm = h.get("alarm")
    if alarm and alarm.get("code") and not alarm.get("in_doc"):
        warn.append("alarm code exists and stays OUT of the printed doc - "
                    "hand over verbally (good)")
    if alarm and alarm.get("code") and alarm.get("in_doc"):
        warn.append("alarm code WILL be printed in the doc - photographs "
                    "of documents travel; prefer verbal handoff")

    wifi = h.get("wifi") or {}
    if not wifi.get("ssid"):
        warn.append("no guest wifi ssid - sitters will ask within the hour")
    if not reg.get("quirks"):
        warn.append("no house quirks listed - every house has some")
    if not reg.get("key_location"):
        warn.append("no key location - how does the sitter get in?")
    for p in pets:
        if p.get("meds", "None").lower() not in ("none", ""):
            if "call" not in json.dumps(p).lower() and not p.get("vet", {}).get("phone"):
                crit.append(f"pet '{p.get('name','?')}' on meds but no vet contact")
    return crit, warn


def find_role(contacts, role):
    for c in contacts:
        if role in (c.get("role") or "").lower():
            return c
    return None


def gen_handoff(reg):
    h = reg.get("household", {})
    L = []
    A = L.append
    A(f"# House Handoff — {h.get('address','(address)')}")
    A("")
    A(f"**Sitter:** {h.get('sitter','?')}  ")
    A(f"**Away:** {h.get('dates','?')}  "
      f"**Generated:** 2026 (keep this sheet where you can find it)")
    A("")
    A("## First 30 minutes (day one)")
    A("")
    A(f"- Get in: {reg.get('key_location','(see owner)')}")
    wifi = h.get("wifi") or {}
    if wifi:
        A(f"- Wifi: `{wifi.get('ssid')}` / `{wifi.get('password','')}`")
    if h.get("thermostat"):
        A(f"- Heating: {h['thermostat']}")
    if reg.get("mail"):
        A(f"- Mail: {reg['mail']}")
    t = reg.get("trash") or {}
    if t:
        days = "/".join(t.get("days", []))
        A(f"- Trash: {days} — {t.get('note','')}")
    alarm = h.get("alarm")
    if alarm:
        if alarm.get("in_doc"):
            A(f"- Alarm ({alarm.get('brand')}): code {alarm.get('code')} "
              f"— arm/disarm demo by owner")
        else:
            A(f"- Alarm ({alarm.get('brand')}): code given verbally/by owner — "
              "test it twice before we leave")
    A("")
    A("## Daily routine")
    for p in reg.get("pets", []):
        A("")
        A(f"### {p.get('name')} ({p.get('species')}, {p.get('age','?')}y)")
        for k, lab in (("feeding", "Feeding"), ("meds", "Medication"),
                       ("litter", "Litter/cleaning"), ("quirks", "Quirks"),
                       ("emergency_note", "Watch for")):
            if p.get(k) and str(p[k]).lower() != "none":
                A(f"- **{lab}:** {p[k]}")
        vet = p.get("vet") or {}
        if vet:
            A(f"- **Vet:** {vet.get('clinic','')} — {vet.get('phone','')}")
    if reg.get("plants"):
        A("")
        A("### Plants")
        for pl in reg["plants"]:
            A(f"- **{pl.get('name')}** ({pl.get('where','')}): {pl.get('water','')}")
    A("")
    A("## House quirks (read twice)")
    for q in reg.get("quirks", []):
        A(f"- {q}")
    A("")
    A("## Shutoffs — know BEFORE you need them")
    for k, v in reg.get("shutoffs", {}).items():
        A(f"- **{k.replace('_',' ').title()}:** {v}")
    A("")
    A("## If something goes wrong")
    for e in reg.get("escalation", []):
        A(f"- **If {e.get('if')}:** {e.get('do')}")
    if reg.get("spending_rule"):
        A(f"- **Spending:** {reg['spending_rule']}")
    A("")
    A("## People")
    for c in reg.get("contacts", []):
        A(f"- **{c.get('role','?')}** — {c.get('name','')}: {c.get('phone','')}")
    return "\n".join(L) + "\n"


def gen_card(reg, region):
    owner = find_role(reg.get("contacts", []), "owner") or {}
    vet = (reg.get("pets") or [{}])[0].get("vet") or {}
    sh = reg.get("shutoffs", {})
    L = []
    A = L.append
    A("# EMERGENCY CARD — fridge")
    A("")
    A(f"House: {(reg.get('household') or {}).get('address','')}")
    A("")
    A(f"**Call owner:** {owner.get('name','')} {owner.get('phone','')}")
    A("")
    A("## Shutoffs NOW")
    A(f"- Water: {sh.get('water_main','ASK OWNER')}")
    A(f"- Power: {sh.get('electricity','ASK OWNER')}")
    A(f"- Gas: {sh.get('gas','ASK OWNER')}")
    A("")
    A("## Vet")
    A(f"{vet.get('clinic','')} {vet.get('phone','')}")
    A("")
    A(f"## Poison line: {POISON_LINES.get(region, POISON_LINES['EU'])}")
    A("")
    A("When unsure: close the water main, leave, call owner.")
    return "\n".join(L) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("registry")
    p.add_argument("--audit-only", action="store_true")
    p.add_argument("--out-dir", default="out")
    p.add_argument("--winter", action="store_true",
                   help="apply winter audit strictness")
    p.add_argument("--region", default="US", choices=list(POISON_LINES))
    a = p.parse_args()

    reg = json.load(open(a.registry, encoding="utf-8"))
    winter = a.winter or reg.get("household", {}).get("winter", False)

    crit, warn = audit(reg, winter)
    print("AUDIT")
    for c in crit:
        print(f"  CRITICAL: {c}")
    for w in warn:
        print(f"  WARN    : {w}")
    if not crit and not warn:
        print("  packet ready - no gaps found")

    if a.audit_only:
        return 1 if crit else 0

    os.makedirs(a.out_dir, exist_ok=True)
    hand = os.path.join(a.out_dir, "HANDOFF.md")
    card = os.path.join(a.out_dir, "EMERGENCY_CARD.md")
    with open(hand, "w", encoding="utf-8") as f:
        f.write(gen_handoff(reg))
    with open(card, "w", encoding="utf-8") as f:
        f.write(gen_card(reg, a.region))
    print(f"wrote {hand}\nwrote {card}")
    if any("WILL be printed" in w for w in warn):
        print("NOTE: alarm code is printed in the doc - prefer verbal handoff.")
    return 1 if crit else 0


if __name__ == "__main__":
    sys.exit(main())
