#!/usr/bin/env python3
"""
generate-passport.py — Med passport generator

Reads meds-state.json and writes a self-contained, print-ready
med-passport.html listing all active medications.

Usage:
    python3 generate-passport.py
    python3 generate-passport.py --name "Jane Smith"
    python3 generate-passport.py --name "Jane Smith" --dob "1975-03-12"
    python3 generate-passport.py --out /path/to/output.html

Environment:
    MEDS_STATE_FILE   path to meds-state.json   (default: same dir as script)

Options:
    --name NAME       Patient name printed on the card (prompted if omitted)
    --dob  DOB        Date of birth (optional, shown on card)
    --out  PATH       Output file path (default: med-passport.html, same dir as state)
    --no-prompt       Skip the name prompt; omit name from card
    --dry-run         Print the HTML to stdout instead of writing a file
"""

import argparse
import html
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
STATE_FILE = Path(os.environ.get("MEDS_STATE_FILE", SCRIPT_DIR / "meds-state.json"))


# ── Formatting helpers ─────────────────────────────────────────────────────────

def fmt_frequency(sched: dict) -> str:
    freq = sched["frequency"]
    if freq == "as_needed":
        return "As needed"
    if freq == "interval":
        h = sched.get("interval_hours", "?")
        return f"Every {h}h"
    times = sched.get("times", [])
    fmt_times = [fmt_12h(t) for t in times]
    labels = {
        "once_daily":  "Once daily",
        "twice_daily": "Twice daily",
        "weekly":      "Weekly",
    }
    base = labels.get(freq, freq.replace("_", " ").title())
    if fmt_times:
        return f"{base} — {', '.join(fmt_times)}"
    return base


def fmt_12h(hhmm: str) -> str:
    h, m = map(int, hhmm.split(":"))
    suffix = "am" if h < 12 else "pm"
    return f"{h % 12 or 12}:{m:02d}{suffix}"


def fmt_date(iso: str) -> str:
    try:
        d = datetime.fromisoformat(iso)
        return d.strftime("%B %d, %Y")
    except Exception:
        return iso


def esc(s: str) -> str:
    return html.escape(str(s or ""))


# ── HTML generation ────────────────────────────────────────────────────────────

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  font-size: 13px;
  background: #f0f4f8;
  color: #1a202c;
  padding: 24px 16px;
  line-height: 1.5;
}

.page {
  max-width: 720px;
  margin: 0 auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 24px rgba(0,0,0,.12);
  overflow: hidden;
}

/* Header */
.passport-header {
  background: #1e3a5f;
  color: #fff;
  padding: 20px 24px 16px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}
.passport-header-left h1 {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: .02em;
  margin-bottom: 2px;
}
.passport-header-left .subtitle {
  font-size: 11px;
  opacity: .7;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.passport-header-right {
  text-align: right;
  font-size: 11px;
  opacity: .75;
  white-space: nowrap;
}
.passport-header-right .patient-name {
  font-size: 15px;
  font-weight: 600;
  opacity: 1;
  margin-bottom: 2px;
}

/* Med table */
.med-table-wrap {
  padding: 20px 24px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: #64748b;
  padding: 0 10px 8px;
  border-bottom: 2px solid #e2e8f0;
  text-align: left;
}

tbody tr {
  border-bottom: 1px solid #f1f5f9;
}
tbody tr:last-child {
  border-bottom: none;
}
tbody tr:hover td {
  background: #f8fafc;
}

tbody td {
  padding: 10px;
  vertical-align: top;
}

td.med-name {
  font-weight: 700;
  font-size: 13px;
  min-width: 120px;
}
td.med-dose {
  font-variant-numeric: tabular-nums;
  color: #1e3a5f;
  font-weight: 600;
  white-space: nowrap;
}
td.med-type {
  color: #64748b;
  font-size: 12px;
  text-transform: capitalize;
}
td.med-freq {
  color: #374151;
}
td.med-food {
  text-align: center;
  color: #16a34a;
  font-size: 15px;
}
td.med-notes {
  color: #64748b;
  font-size: 12px;
  max-width: 160px;
}

.empty-note {
  color: #cbd5e1;
}

/* Status badges */
.badge {
  display: inline-block;
  padding: 1px 7px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .04em;
}

/* Footer */
.passport-footer {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: #94a3b8;
}
.passport-footer strong {
  color: #475569;
}

/* Emergency note */
.emergency-note {
  margin: 0 24px 16px;
  padding: 10px 14px;
  background: #fef3c7;
  border-left: 3px solid #f59e0b;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  color: #78350f;
}

/* Print styles */
@media print {
  body {
    background: #fff;
    padding: 0;
  }
  .page {
    box-shadow: none;
    border-radius: 0;
    max-width: 100%;
  }
  .no-print {
    display: none !important;
  }
  tbody tr:hover td {
    background: transparent;
  }
  @page {
    margin: 1cm;
    size: A5 landscape;
  }
}
"""

SCREEN_CONTROLS = """
<div class="no-print" style="max-width:720px;margin:0 auto 16px;
     display:flex;justify-content:flex-end;gap:8px;">
  <button onclick="window.print()"
    style="padding:8px 16px;background:#1e3a5f;color:#fff;border:none;
           border-radius:6px;font-size:13px;cursor:pointer;font-weight:500">
    Print / Save PDF
  </button>
</div>
"""


def build_html(state: dict, patient_name: str, dob: str) -> str:
    meds = [m for m in state["meds"] if not m.get("paused")]
    generated = datetime.now(tz=timezone.utc).strftime("%B %d, %Y")

    # Header
    header_right = []
    if patient_name:
        header_right.append(f'<div class="patient-name">{esc(patient_name)}</div>')
    if dob:
        header_right.append(f'<div>DOB: {esc(dob)}</div>')
    header_right.append(f'<div>Generated: {generated}</div>')

    # Medication rows
    if meds:
        rows = []
        for med in meds:
            sched = med["schedule"]
            food_icon = "✓" if sched.get("with_food") else ""
            notes = esc(sched.get("notes") or "")
            notes_cell = notes if notes else '<span class="empty-note">—</span>'

            rows.append(f"""
        <tr>
          <td class="med-name">{esc(med['name'])}</td>
          <td class="med-dose">{esc(med['dose'])}{esc(med['unit'])}</td>
          <td class="med-type">{esc(med['type'])}</td>
          <td class="med-freq">{esc(fmt_frequency(sched))}</td>
          <td class="med-food">{food_icon}</td>
          <td class="med-notes">{notes_cell}</td>
        </tr>""")

        table_html = f"""
    <table>
      <thead>
        <tr>
          <th>Medication</th>
          <th>Dose</th>
          <th>Form</th>
          <th>Schedule</th>
          <th>With food</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>{''.join(rows)}
      </tbody>
    </table>"""
    else:
        table_html = '<p style="color:#94a3b8;text-align:center;padding:24px">No active medications.</p>'

    paused_count = len(state["meds"]) - len(meds)
    paused_note = (
        f'<div class="emergency-note">⚠️ {paused_count} medication(s) currently paused — '
        f'confirm with prescriber before resuming.</div>'
        if paused_count else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Medication Passport{" — " + esc(patient_name) if patient_name else ""}</title>
<style>{CSS}</style>
</head>
<body>

{SCREEN_CONTROLS}

<div class="page">
  <div class="passport-header">
    <div class="passport-header-left">
      <div class="subtitle">Medication Passport</div>
      <h1>Active Medications</h1>
    </div>
    <div class="passport-header-right">
      {''.join(header_right)}
    </div>
  </div>

  {paused_note}

  <div class="med-table-wrap">
    {table_html}
  </div>

  <div class="passport-footer">
    <span>Generated by Med Reminder &nbsp;·&nbsp; Keep with emergency contacts</span>
    <strong>{len(meds)} active med{"s" if len(meds) != 1 else ""}</strong>
  </div>
</div>

</body>
</html>"""


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a printable med passport HTML from meds-state.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--name",      default="", help="Patient name")
    parser.add_argument("--dob",       default="", help="Date of birth (optional)")
    parser.add_argument("--out",       default="", help="Output file path")
    parser.add_argument("--no-prompt", action="store_true",
                        help="Skip name prompt; omit name from card")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print HTML to stdout instead of writing a file")
    args = parser.parse_args()

    if not STATE_FILE.exists():
        sys.exit(
            f"State file not found: {STATE_FILE}\n"
            "Run: cp meds-state.template.json meds-state.json"
        )

    with STATE_FILE.open(encoding="utf-8") as f:
        state = json.load(f)

    patient_name = args.name.strip()
    if not patient_name and not args.no_prompt and not args.dry_run:
        try:
            patient_name = input("Patient name (leave blank to omit): ").strip()
        except (EOFError, KeyboardInterrupt):
            patient_name = ""

    dob = args.dob.strip()

    page = build_html(state, patient_name, dob)

    if args.dry_run:
        print(page)
        return

    out_path = Path(args.out) if args.out else STATE_FILE.parent / "med-passport.html"
    out_path.write_text(page, encoding="utf-8")
    print(f"Med passport saved to {out_path}")
    print(f"  {len([m for m in state['meds'] if not m.get('paused')])} active med(s) included")
    if any(m.get("paused") for m in state["meds"]):
        skipped = sum(1 for m in state["meds"] if m.get("paused"))
        print(f"  {skipped} paused med(s) excluded")
    print("Open in a browser and use Print > Save as PDF to share.")


if __name__ == "__main__":
    main()
