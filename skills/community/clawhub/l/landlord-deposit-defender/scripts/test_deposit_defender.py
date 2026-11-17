#!/usr/bin/env python3
"""Tests for landlord-deposit-defender.

Run:  python3 scripts/test_deposit_defender.py
Plain asserts with [PASS] lines; exits 0 and prints ALL TESTS PASSED.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "deposit_defender.py")
PY = sys.executable or "python3"

passed = 0
failed = 0


def run(args, expect_rc=0):
    """Run the CLI with args; assert returncode matches; return CompletedProcess."""
    global failed
    proc = subprocess.run(
        [PY, SCRIPT] + args, capture_output=True, text=True, timeout=60
    )
    if proc.returncode != expect_rc:
        failed += 1
        print(f"[FAIL] rc={proc.returncode} (expected {expect_rc}) for: {args}")
        print("  stdout:", proc.stdout[:600])
        print("  stderr:", proc.stderr[:600])
        raise SystemExit(f"command failed: {args}\n{proc.stdout}\n{proc.stderr}")
    return proc


def check(name, condition, detail=""):
    """Record one assertion result."""
    global passed, failed
    if condition:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name} {detail}")


# ---------------------------------------------------------------------------
# 1. Grade validation (inventory rejects bad grades)
# ---------------------------------------------------------------------------
proc = run(["inventory", "--item", "Kitchen,Countertop,9,way out of range"],
           expect_rc=2)
check("grade 9 rejected with error", "grade must be an integer 0-5" in proc.stderr)

proc = run(["inventory", "--item", "Kitchen,Countertop,x,not a number"],
           expect_rc=2)
check("non-integer grade rejected", "grade must be an integer 0-5" in proc.stderr)

proc = run(["inventory", "--item", "Kitchen,Countertop,-1,negative"], expect_rc=2)
check("negative grade rejected", "grade must be an integer 0-5" in proc.stderr)

# ---------------------------------------------------------------------------
# 2. Inventory builds + JSON round-trip
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    move_in_path = os.path.join(tmp, "move_in.json")
    proc = run([
        "inventory", "--label", "move-in", "--date", "2024-03-01", "--json",
        "--item", "Living Room,Carpet,1,professionally cleaned before move-in",
        "--item", "Living Room,Paint,1,fresh builder white",
        "--item", "Kitchen,Blinds,1,new vinyl",
        "--item", "Bedroom,Curtains,2,light sun fade on south wall",
    ])
    inv = json.loads(proc.stdout)
    check("inventory json has label", inv["label"] == "move-in")
    check("inventory grades in range", inv["grade_range"] == [1, 2])
    with open(move_in_path, "w") as fh:
        fh.write(proc.stdout)
    # Round-trip: the file written to disk loads back through the CLI.
    proc2 = run(["diff", "--move-in", move_in_path, "--move-out", move_in_path, "--json"])
    rt = json.loads(proc2.stdout)
    check("inventory JSON round-trips through diff",
          rt["summary"]["items_compared"] == 4 and rt["summary"]["unchanged"] == 4)

    # -----------------------------------------------------------------------
    # 3. Diff classification: wear vs damage vs improvement
    # -----------------------------------------------------------------------
    move_out_path = os.path.join(tmp, "move_out.json")
    proc = run([
        "inventory", "--label", "move-out", "--date", "2026-03-01", "--json",
        "--item", "Living Room,Carpet,3,flattened pile and worn traffic pattern",
        "--item", "Living Room,Paint,2,scuffed and faded near switches",
        "--item", "Kitchen,Blinds,1,undamaged",
        "--item", "Bedroom,Curtains,1,newly professionally cleaned curtains",
    ])
    with open(move_out_path, "w") as fh:
        fh.write(proc.stdout)

    proc = run([
        "diff", "--move-in", move_in_path, "--move-out", move_out_path,
        "--tenancy-start", "2024-03-01", "--tenancy-end", "2026-03-01", "--json",
    ])
    diff = json.loads(proc.stdout)
    classes = {row["item"]: row["classification"] for row in diff["items"]}

    # carpet: worn traffic pattern + age 2y < life 8y, delta=2, no damage keyword
    # -> keyword 'worn' hits WEAR first
    check("carpet matting classified as wear", classes.get("Carpet") == "wear")
    # paint: 'scuffed' keyword -> wear
    check("paint scuffs classified as wear", classes.get("Paint") == "wear")
    # curtains cleaned at tenant expense: grade 2 -> 1 = improvement
    check("curtains cleaned = improvement", classes.get("Curtains") == "improvement")
    check("blinds unchanged", classes.get("Blinds") == "unchanged")
    check("diff computed tenancy years 2.0",
          abs(diff["summary"]["tenancy_years"] - 2.0) < 0.01)

    # Damage: cigarette burn + a missing item.
    dmg_in = os.path.join(tmp, "dmg_in.json")
    dmg_out = os.path.join(tmp, "dmg_out.json")
    run(["inventory", "--date", "2024-03-01", "--json",
         "--item", "Bedroom,Carpet,1,clean", "--item", "Hallway,Door,1,ok",
         "--item", "Kitchen,Smoke Detector,0,new"])
    with open(dmg_in, "w") as fh:
        fh.write(run(["inventory", "--date", "2024-03-01", "--json",
                      "--item", "Bedroom,Carpet,1,clean",
                      "--item", "Hallway,Door,1,ok",
                      "--item", "Kitchen,Smoke Detector,0,new"]).stdout)
    with open(dmg_out, "w") as fh:
        fh.write(run(["inventory", "--date", "2026-03-01", "--json",
                      "--item", "Bedroom,Carpet,3,cigarette burn near bed",
                      "--item", "Hallway,Door,2,small crack",
                      # smoke detector simply omitted -> missing-at-move-out
                      ]).stdout)
    proc = run(["diff", "--move-in", dmg_in, "--move-out", dmg_out,
                "--tenancy-start", "2024-03-01", "--tenancy-end", "2026-03-01",
                "--json"])
    diff2 = json.loads(proc.stdout)
    classes2 = {row["item"]: row["classification"] for row in diff2["items"]}
    check("cigarette burn classified as damage", classes2.get("Carpet") == "damage")
    check("missing smoke detector flagged", any(
        row["direction"] == "missing-at-move-out" and row["disputable"] is False
        for row in diff2["items"]))
    check("crack keyword classified as damage", classes2.get("Door") == "damage")

    # -----------------------------------------------------------------------
    # 4. Proration formula
    # ---------------------------------------------------------------------------
    proc = run(["prorate", "--tenancy-years", "2",
                "--item", "carpet,1200,8,1200", "--json"])
    pr = json.loads(proc.stdout)
    row = pr["items"][0]
    check("carpet 1200 8y life 2y used -> legit 900",
          abs(row["max_legitimate_deduction"] - 900.0) < 0.01,
          f"got {row['max_legitimate_deduction']}")
    check("carpet full-price demand flagged as over-demand",
          row["over_demand"] is True and row["demanded"] == 1200.0)

    # Fully depreciated -> zero.
    proc = run(["prorate", "--tenancy-years", "8",
                "--item", "carpet,1200,8,1200", "--json"])
    row = json.loads(proc.stdout)["items"][0]
    check("carpet fully depreciated -> 0 deduction",
          row["max_legitimate_deduction"] == 0.0 and row["fully_depreciated"] is True)

    # Over-demand detection: landlord demands full replacement price.
    proc = run(["prorate", "--tenancy-years", "2",
                "--item", "paint,800,3,800", "--json"])
    row = json.loads(proc.stdout)["items"][0]
    # 800 * (1 - 2/3) = 266.67 demanded 800 -> over-demand
    check("paint over-demand flagged", row["over_demand"] is True)
    check("paint legit = 266.67",
          abs(row["max_legitimate_deduction"] - 266.67) < 0.01)

    # --depreciated: pre-aged item, age 5 of 10y life, value 600
    proc = run(["prorate", "--depreciated",
                "--item", "vinyl flooring,600,10,5", "--json"])
    row = json.loads(proc.stdout)["items"][0]
    check("--depreciated pre-aged item: 600*(1-5/10)=300",
          abs(row["max_legitimate_deduction"] - 300.0) < 0.01)

    # ---------------------------------------------------------------------------
    # 5. Jurisdiction lookup
    # ---------------------------------------------------------------------------
    proc = run(["jurisdictions", "--json"])
    table = json.loads(proc.stdout)["jurisdictions"]
    check("jurisdictions table has >= 15 entries", len(table) >= 15, f"got {len(table)}")
    check("US-CA deadline 21 days", table["US-CA"]["days"] == 21)
    check("GB deadline 10 days", table["GB"]["days"] == 10)
    check("US-FL uses 15-60 day window", table["US-FL"]["window"] == [15, 60])

    # Unknown jurisdiction rejected.
    proc = run(["letter", "--move-in", move_in_path, "--move-out", move_out_path,
                "--deposit", "2400", "--deductions", "/dev/null/nonexistent.json",
                "--jurisdiction", "XX"], expect_rc=2)
    check("unknown jurisdiction rejected", "unknown jurisdiction" in proc.stderr)

    # ---------------------------------------------------------------------------
    # 6. Letter generation
    # ---------------------------------------------------------------------------
    ded_path = os.path.join(tmp, "deductions.json")
    with open(ded_path, "w") as fh:
        json.dump([
            {"item": "Carpet", "amount": 1200,
             "reason": "replacement of worn carpet"},
            {"item": "Paint", "amount": 800,
             "reason": "repaint after scuffs"},
            {"item": "Rug", "amount": 1200,
             "reason": "candle wax burn, replaced"},
        ], fh)

    proc = run([
        "letter",
        "--move-in", move_in_path,
        "--move-out", move_out_path,
        "--deposit", "2400",
        "deductions", ded_path,
        "--jurisdiction", "CA",
        "--tenant", "Jordan Reyes",
        "--landlord", "Acme Property Mgmt",
    ], expect_rc=2)
    check("letter rejects stray positional 'deductions'",
          "error" in proc.stderr and proc.returncode == 2)

    proc = run([
        "letter",
        "--move-in", move_in_path, "--move-out", move_out_path,
        "--deposit", "2400", "--deductions", ded_path,
        "--jurisdiction", "CA", "--tenant", "Jordan Reyes",
        "--landlord", "Acme Property Mgmt", "--json",
    ])
    letter = json.loads(proc.stdout)
    md = letter["letter_markdown"]
    a = letter["analysis"]
    check("letter has Timeline section", "## 1. Timeline" in md)
    check("letter has itemized rebuttal section", "## 3. Itemized rebuttal" in md)
    check("letter has documents/receipts demand", "## 4. Documents requested" in md)
    check("letter has escalation notice", "small-claims" in md)
    check("letter cites CA deadline", "21 days" in a["deadline_line"])
    check("letter contains tenant name", "Jordan Reyes" in md)
    check("letter contains prorated amount 900.00", "900.00" in md)
    check("letter refund due = deposit - fair total",
          abs(a["refund_due"] - (2400 - a["max_legitimate_total"])) < 0.01)
    # Carpet wear -> 0; paint wear -> 0; rug burn (carpet-class, 8y life,
    # 2y used) -> 1200 * 0.75 = 900
    check("letter fair total = 900.00 (wear items 0, rug prorated)",
          abs(a["max_legitimate_total"] - 900.0) < 0.01,
          f"got {a['max_legitimate_total']}")

    # ---------------------------------------------------------------------------
    # 7. Date math
    # ---------------------------------------------------------------------------
    proc = run(["diff", "--in-item", "A,B,1", "--out-item", "A,B,2",
                "--tenancy-start", "2023-06-15", "--tenancy-end", "2026-06-15",
                "--json"])
    d = json.loads(proc.stdout)
    check("tenancy date math ~3.0 years over leap span",
          abs(d["summary"]["tenancy_years"] - 3.0) < 0.02)
    check("unjustified 1-grade deterioration defaults to wear",
          d["items"][0]["classification"] == "wear")

    # Reversed dates rejected.
    proc = run(["diff", "--in-item", "A,B,1", "--out-item", "A,B,2",
                "--tenancy-start", "2026-01-01", "--tenancy-end", "2024-01-01"],
               expect_rc=2)
    check("reversed tenancy dates rejected",
          "before --tenancy-start" in proc.stderr)

    # Malformed date rejected.
    proc = run(["inventory", "--item", "A,B,1", "--date", "2024-13-99"], expect_rc=2)
    check("malformed date rejected", "YYYY-MM-DD" in proc.stderr)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
if failed == 0:
    print(f"ALL TESTS PASSED ({passed} assertions)")
    sys.exit(0)
print(f"FAILED: {failed} of {passed + failed} assertions")
sys.exit(1)
