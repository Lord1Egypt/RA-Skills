#!/usr/bin/env python3
"""medtravel.py — medication travel screener (offline, rule-based).

Subcommands:
  screen    per-medication travel verdicts (controlled/cold-chain/liquids/
            supply math/destination gates)
  schedule  timezone-shift dosing plan
  letter    doctor-letter request (required elements + email draft)
  packing   packing checklist by flags

No third-party deps. Not medical advice: it flags and plans, it never
prescribes or changes doses.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- knowledge base

CONTROLLED = [
    # (regex, schedule, class label)
    (r"adderall|amphet|lisdexam|elvanse|mydayis", "II", "stimulant (amphetamine-class)"),
    (r"methylphenidate|ritalin|concerta|focalin", "II", "stimulant (methylphenidate)"),
    (r"oxycodone|oxycontin|morphine|fentanyl|hydromorphone|dilaudid", "II", "opioid"),
    (r"\bcodeine\b", "II/III", "opioid (codeine) — schedule varies by country/product"),
    (r"testosterone|cypionate|enanthate|androgel", "III", "anabolic/androgen"),
    (r"ketamine", "III", "dissociative anesthetic"),
    (r"alprazolam|xanax", "IV", "benzodiazepine"),
    (r"lorazepam|ativan", "IV", "benzodiazepine"),
    (r"diazepam|valium", "IV", "benzodiazepine"),
    (r"clonazepam|klonopin", "IV", "benzodiazepine"),
    (r"tramadol|ultram", "IV", "opioid-like"),
    (r"zolpidem|ambien|eszopiclone|lunesta|zopiclone", "IV", "hypnotic (Z-drug)"),
    (r"modafinil|provigil|armodafinil", "IV", "wakefulness agent"),
    (r"pregabalin|lyrica|gabapentin", "V*", "gabapentinoid (state/country dependent)"),
]

COLD_CHAIN = [
    # (regex, in-use days at room temp, note)
    (r"tresiba|degludec", 56, "Longest in-use window — best basal for very long trips."),
    (r"insulin|lantus|levemir|detemir|humalog|lispro|novorapid|aspart|glulisine|toujeo", 28, "Never freeze. Never checked hold. Never glovebox/dash."),
    (r"ozempic|semaglutide|rybelsus", 28, "Rybelsus is oral: no fridge needed in use."),
    (r"mounjaro|tirzepatide|zepbound", 21, ""),
    (r"victoza|liraglutide|saxenda|trulicity|dulaglutide|byetta|bydureon", 28, ""),
    (r"humira|adalimumab|enbrel|etanercept|remicade|infliximab|cosentyx|secukinumab|stelara|ustekinumab", 14, "Biologic: 14 days ≤25°C typical in-use window."),
]

# destination gates: regex on med name -> advisory
DESTINATION_GATES = {
    "japan": [
        (r"amphet|adderall|lisdexam|methylphenidate|ritalin|concerta|focalin|modafinil",
         "PROHIBITED-class: amphetamine/methylphenidate stimulants are treated as narcotics. "
         "Import requires advance Yakkan Shoumei certificate (~2 months via MHLW). "
         "Confirm with the Japanese embassy BEFORE booking — do not carry it and hope."),
        (r"pseudoephedrine|sudafed",
         "Restricted OTC decongestant — amounts over personal limits need certification."),
        (r"codeine",
         "Codeine products: import notification required; some OTC combos banned."),
    ],
    "uae": [
        (r"amphet|adderall|methylphenidate|alprazolam|xanax|diazepam|valium|lorazepam|ativan|"
         r"clonazepam|zolpidem|ambien|tramadol|codeine|testosterone",
         "Psychotropics/narcotics require MOHAP pre-approval + original prescription + "
         "doctor letter (attested translation helps). Carry in original container, declare."),
    ],
    "saudi": [
        (r"amphet|adderall|alprazolam|xanax|diazepam|zolpidem|tramadol|codeine",
         "SFDA approval needed for most psychotropics; check embassy list before flying."),
    ],
    "qatar": [
        (r"amphet|adderall|alprazolam|xanax|diazepam|tramadol|codeine",
         "Ministry of Public Health permit required for controlled psychotropics."),
    ],
    "singapore": [
        (r"alprazolam|xanax|diazepam|valium|lorazepam|zolpidem|ambien|eszopiclone|zopiclone",
         "HSA license required for sleeping pills/anxiolytics; apply ahead."),
        (r"codeine", "Codeine restrictions — prescription + letter required."),
    ],
    "china": [
        (r"amphet|adderall|methylphenidate|alprazolam|diazepam|zolpidem",
         "Strictly controlled: certificate from Chinese authorities required."),
    ],
    "greece": [
        (r"codeine|tramadol",
         "Controlled in Greece: carry prescription + doctor letter."),
    ],
    "russia": [
        (r"codeine|tramadol",
         "Prescription drugs containing these are controlled — carry prescription copy; "
         "some formulations banned; check embassy list."),
    ],
    "indonesia": [
        (r"codeine|tramadol|diazepam|alprazolam",
         "Some controlled meds require prior approval (BPOM/embassy confirmation)."),
    ],
    "egypt": [
        (r"tramadol|codeine|adderall",
         "Tramadol is strictly banned; other controlled meds need embassy letter."),
    ],
}

LIQUID_RE = re.compile(r"\bml\b|suspension|syrup|solution|inject|pen\b|vial|drops\b|liquid")

FOOTER = ("\nNOT MEDICAL ADVICE — flags and logistics only. Doses stay as "
          "prescribed; verify anything borderline with your pharmacist or doctor.\n")


@dataclass
class MedVerdict:
    name: str
    lines: list = field(default_factory=list)
    blockers: int = 0
    cold_chain: bool = False
    controlled: str = ""


def parse_meds(raw: str):
    meds = []
    for chunk in re.split(r"[;,\n]+", raw or ""):
        chunk = chunk.strip()
        if chunk:
            meds.append(chunk)
    return meds


def doses_per_day(name: str) -> float:
    m = re.search(r"(\d+)\s*x\s*(?:a\s*)?day|once\s*daily|daily", name, re.I)
    if re.search(r"once\s*daily|1\s*x", name, re.I):
        return 1
    m = re.search(r"(\d+)\s*x", name)
    if m:
        return float(m.group(1))
    if re.search(r"daily|every\s*day", name, re.I):
        return 1
    return 1  # unknown → assume 1/day, flagged in output


def screen(meds, days, destination, on_hand):
    dest = (destination or "").strip().lower()
    gates = DESTINATION_GATES.get(dest)
    if dest and dest not in DESTINATION_GATES:
        print(f"[i] No destination gate data for '{destination}' — default rule for "
              f"Schedule II/III drugs: verify with the embassy.\n")
    verdicts = []
    print(f"MEDICATION TRAVEL SCREEN — {days} days"
          + (f" → {destination.upper()}" if dest else ""))
    print("═" * 62)
    for i, med in enumerate(meds, 1):
        low = med.lower()
        v = MedVerdict(name=med)
        print(f"[{i}] {med}")
        # controlled?
        for rx, sched, label in CONTROLLED:
            if re.search(rx, low):
                v.controlled = sched
                v.lines.append(
                    f"  ⚠ CONTROLLED — Schedule {sched} ({label}).\n"
                    f"     → Original labeled container + doctor letter; keep count = Rx; "
                    f"declare at borders.")
                break
        # destination gate?
        if gates:
            for rx, advice in gates:
                if re.search(rx, low):
                    v.blockers += 1
                    v.lines.append(f"  ✖ DESTINATION GATE: {advice}")
                    break
        # cold chain?
        for rx, in_use, note in COLD_CHAIN:
            if re.search(rx, low):
                v.cold_chain = True
                v.lines.append(
                    f"  ❄ COLD CHAIN — carry-on ONLY, never checked.\n"
                    f"     Unopened: 2–8°C. In use: {in_use} days at room temp (≤30°C). {note}")
                break
        # liquid?
        if LIQUID_RE.search(low):
            v.lines.append(
                "  💧 LIQUID/INJECTABLE — medically necessary liquids are exempt from the "
                "100 mL rule but must be DECLARED at screening. Gel packs: allowed, say so first.")
        # supply math
        dpd = doses_per_day(low)
        need = days * dpd
        have = on_hand
        if have is not None:
            if have < need:
                v.lines.append(
                    f"  📦 SUPPLY: need ~{need:.0f} doses for {days} days, have {have:.0f} "
                    f"→ EARLY REFILL required (+{need - have:.0f}). Say 'vacation override' "
                    f"to the insurer; controlled scripts need the prescriber to file it.")
            else:
                v.lines.append(f"  ✔ Supply: need ~{need:.0f}, have {have:.0f} — OK.")
        # insulin in-use clock
        if re.search(r"insulin|lantus|humalog|novorapid|tresiba|toujeo", low) and days > 28:
            v.lines.append(
                "  ⏱ IN-USE CLOCK: trip > 28 days — if the pen is already opened, it will "
                "expire mid-trip. Bring a new sealed pen (fridge rules) as the travel unit.")
        for ln in v.lines:
            print(ln)
        verdicts.append(v)
        print()
    blockers = sum(v.blockers for v in verdicts)
    cold = sum(v.cold_chain for v in verdicts)
    ctrl = sum(1 for v in verdicts if v.controlled)
    print("─" * 62)
    print(f"VERDICT: {blockers} BLOCKER(S), {ctrl} controlled, {cold} cold-chain item(s).")
    if blockers:
        print("ACTION: resolve destination gates (embassy confirmation) BEFORE booking.")
    if ctrl or cold:
        print("ACTION: run `letter` and `packing` subcommands next.")
    print("RULE OF TWO: split all critical meds across two bags + 2 spare days.")
    print(FOOTER)
    return verdicts


def schedule(med, from_tz, to_tz):
    shift = to_tz - from_tz
    hours = abs(shift)
    direction = "later" if shift > 0 else "earlier"
    low = med.lower()
    print(f"TIMEZONE DOSING PLAN — '{med}'")
    print(f"Shift: {from_tz:+g} → {to_tz:+g} = {shift:+g} h ({hours:g} h {direction} local).")
    print("═" * 62)
    dpd = doses_per_day(low)
    if re.search(r"insulin|lantus|levemir|tresiba|toujeo|degludec", low):
        print("BASAL INSULIN doctrine:")
        print(f"  • Trip ≤3 days: stay on HOME-clock time entirely.")
        print(f"  • Longer: shift {hours} h in 2–3 h/day steps toward destination time.")
        print("  • NEVER take two basal doses close together; monitor glucose more often.")
    elif re.search(r"birth control|contraceptive|ethinyl|levonorgestrel|norgestimate", low):
        print("FIXED-INTERVAL doctrine (birth control):")
        print("  • Keep a phone alarm on HOME-clock time for the whole trip.")
        print("  • Interval must never exceed 24 h (combined pill) / 36 h (progestin-only).")
        print(f"  • A shift of {hours} h is safe ONLY if you take the pill on home-clock time.")
    elif dpd >= 2:
        print(f"TWICE-DAILY doctrine (detected ≈{dpd:.0f} doses/day):")
        print("  • Keep at least 8 h between doses at all times.")
        print(f"  • Travel day: one interval may stretch to 8–14 h (or compress to 8 h), "
              f"then resume normal spacing on destination time.")
        print("  • Example: 08:00/20:00 home → take 08:00 home-clock, then next dose on "
              "arrival at the first slot that is ≥8 h later.")
    else:
        print("ONCE-DAILY doctrine:")
        if hours <= 4:
            print(f"  • {hours} h shift: on arrival, take the next dose at the new local time "
                  f"(interval will be {24 - hours if shift > 0 else 24 + hours:.0f}–"
                  f"{24 + hours:.0f} h — acceptable for most once-daily drugs).")
        else:
            print(f"  • {hours} h shift: either (a) ±1 h/day ladder starting 3–5 days before "
                  f"the trip, or (b) single adjusted dose so the gap stays inside 18–30 h.")
            print("  • NEVER double up a skipped/moved dose.")
    print("  • Levothyroxine/warfarin/digoxin-style narrow drugs: ask the pharmacist "
          "before improvising — the ladder (a) is the safe default.")
    print(FOOTER)


LETTER_ELEMENTS = [
    "Doctor letterhead with license number and contact",
    "Patient full name EXACTLY as in passport + date of birth",
    "Each medication: brand + generic name, dose, form, frequency",
    "Statement: 'prescribed for the patient's ongoing medical condition'",
    "Signature and date (issued within ~30 days of travel)",
]

EMAIL_TMPL = """Subject: Travel letter request — {meds_summary}

Hello,

I'm traveling for {days} days and need a travel letter covering the
prescription medications below. Please include, per item: brand and generic
name, dose, form and frequency, plus the statement that they are prescribed
for my ongoing condition, your license number and contact, signed and dated.

Medications:
{med_list}

I'll pick it up / would appreciate it by email before {deadline_note}.

Thank you,
{name_note}
"""


def letter(meds, days):
    print("DOCTOR'S LETTER — required elements checklist")
    print("═" * 62)
    for i, e in enumerate(LETTER_ELEMENTS, 1):
        print(f"  [{i}] {e}")
    print()
    print("Request email draft (edit the {placeholders}):")
    print("─" * 62)
    print(EMAIL_TMPL.format(
        meds_summary=(meds[0] + (" + others" if len(meds) > 1 else "")) if meds else "medications",
        days=days,
        med_list="\n".join(f"  - {m}" for m in meds) or "  - (list your medications)",
        deadline_note="(date — ask ≥2 weeks before travel; controlled substances take longer)",
        name_note="(your name)",
    ))
    print("TIP: For UAE/Saudi/Qatar ask whether the clinic can provide the letter "
          "on official letterhead with a stamp — some embassies expect it notarized.")


def packing(cold_chain, controlled, days):
    base = [
        "ALL critical meds in carry-on — never checked (hold freezes/delays).",
        f"Rule of two: supply split across two bags, +2 spare days beyond {days}.",
        "Original labeled containers for everything (pill organizers ride EMPTY).",
        "Photo of every label + e-copy of prescriptions in the phone and cloud.",
        "Pharmacy printout of active prescriptions (ask the pharmacist).",
    ]
    cold = [
        "Frio evaporative pouch (activate in water) OR insulated pouch + 1 gel pack "
        "wrapped in cloth (never direct contact — local freezing kills protein drugs).",
        "Liquid thermometer for hotel fridges — many run below 2°C; use the door shelf "
        "or wrap the pen in a sock.",
        "In-use timer: write the open date on the pen; know its room-temp expiry.",
    ]
    ctrl = [
        "Doctor letter (see `letter`), original containers, count = prescription.",
        "Embassy confirmation printout if any destination gate was flagged.",
        "Declare at immigration before being asked — proactive beats defensive.",
    ]
    for title, items in [("BASE", base),
                         ("COLD CHAIN" if cold_chain else None, cold if cold_chain else None),
                         ("CONTROLLED" if controlled else None, ctrl if controlled else None)]:
        if title:
            print(f"PACKING — {title}")
            for it in items:
                print(f"  • {it}")
            print()
    print("Departure-day: take meds in hand luggage through screening; declare liquids "
          "and gel packs FIRST at the checkpoint. Keep the letter in the same pouch.")
    print(FOOTER)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("screen", help="screen a med list for travel")
    p.add_argument("--meds", required=True,
                   help="semicolon-separated list, e.g. 'Adderall 20mg 2x daily; Lantus insulin'")
    p.add_argument("--days", type=int, required=True)
    p.add_argument("--destination", default="",
                   help="country keyword: japan, uae, singapore, china, ...")
    p.add_argument("--pills-on-hand", type=float, default=None,
                   help="doses currently on hand for supply math")

    p = sub.add_parser("schedule", help="timezone shift plan")
    p.add_argument("--med", required=True)
    p.add_argument("--from-tz", type=float, required=True, help="e.g. 2")
    p.add_argument("--to-tz", type=float, required=True, help="e.g. -5")

    p = sub.add_parser("letter", help="doctor letter elements + email draft")
    p.add_argument("--meds", required=True)
    p.add_argument("--days", type=int, default=14)

    p = sub.add_parser("packing", help="packing checklist")
    p.add_argument("--cold-chain", action="store_true")
    p.add_argument("--controlled", action="store_true")
    p.add_argument("--days", type=int, default=14)

    a = ap.parse_args()
    if a.cmd == "screen":
        screen(parse_meds(a.meds), a.days, a.destination, a.pills_on_hand)
    elif a.cmd == "schedule":
        schedule(a.med, a.from_tz, a.to_tz)
    elif a.cmd == "letter":
        letter(parse_meds(a.meds), a.days)
    elif a.cmd == "packing":
        packing(a.cold_chain, a.controlled, a.days)


if __name__ == "__main__":
    main()
