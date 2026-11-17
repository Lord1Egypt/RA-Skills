#!/usr/bin/env python3
"""hoa-nightmare-navigator — violation letters, fine reasonableness, assessment
projections, and records requests for HOA/condo owners. Stdlib only.

Subcommands: violation, fine, assessments, records, --demo
"""
import argparse

STATE_RULES = {
    "CA": {"statute": "Davis-Stirling Act (Civ. Code §4800–§5860)",
           "fine_rule": "Fines require an adopted schedule (§5850), 14-day written "
                        "notice, and a hearing before the fine is effective (§5710 "
                        "pre-§5310 notice requirements). No schedule = no fine.",
           "records": "Civ. Code §5200–§5260: member inspection of accounting books, "
                      "minutes, contracts, budgets; 5 business days for written "
                      "production of a specific record.",
           "adr": "Civ. Code §5930: ADR must be offered before filing an enforcement "
                  "action (save attorney-fee fights)."},
    "FL": {"statute": "Ch. 720 (HOAs) / Ch. 718 (condos)",
           "fine_rule": "§720.305: 14-day written notice and opportunity for hearing; "
                        "fines capped at $1,000 in the aggregate per violation "
                        "(condos: §718.303, committee approval if appointed).",
           "records": "§720.303(4)-(5): official records open to members within "
                      "5 business days of written request.",
           "adr": "§720.511: pre-suit mediation required for HOA/owner disputes."},
    "TX": {"statute": "Prop. Code Ch. 209 (Residential Subdivisions)",
           "fine_rule": "§209.006-ish regime: violation notice with 30-day cure "
                        "window before fines; hearings on request; schedules must "
                        "be reasonably related (see current text).",
           "records": "§209.005: books and records available to owners; management "
                      "certificates filed with the county.",
           "adr": "No universal ADR gate, but assessment-foreclosure limits apply "
                  "(§209.0063 restraining orders)."},
    "OTHER": {"statute": "your state's common-interest-ownership / POA statute "
                         "(uniform acts in ~half the states)",
           "fine_rule": "Reasonableness doctrine: fines must be in an adopted "
                        "schedule, preceded by notice, and usually a hearing; "
                        "check governing documents for caps.",
           "records": "Most uniform acts grant member inspection rights; cite "
                      "your bylaws article on records plus the statute.",
           "adr": "Check for a pre-litigation ADR requirement in your act."},
}


def cmd_violation(a) -> None:
    rule = STATE_RULES.get(a.state.upper(), STATE_RULES["OTHER"])
    fine_line = (f"a fine of ${a.fine:.0f}" if a.fine else "no fine (yet)")
    letter = f"""[Your name / lot address]
[Association name] — Board of Directors
Re: Response to Violation Notice dated [DATE] — {a.violation!r}

Sent via certified mail and email. Response deadline: [DATE, within {a.deadline_days} days].

Dear Board,

I received a notice citing violation of {a.ccr} ({fine_line}). Before any
further action, I request written answers and process under the governing
documents and {rule['statute']}:

1. The exact text of the covenant/rule alleged violated ({a.ccr}), its
   adoption or amendment date, and where the adopted fine schedule is published.
2. The evidence relied on (photo with date/time, complainant record if the
   documents require producing it).
3. The cure period available and confirmation that no fine accrues while this
   response and any hearing is pending.
4. A hearing date under the notice-and-hearing provisions. {rule['fine_rule']}
5. If the board treats this as architectural: the denial findings the ARC is
   required to issue (reasons, standards applied).

I intend to cure or contest properly and ask the board to respond within
14 days. {'If a fine has been levied without notice or hearing, I demand its reversal.' if a.fine else ''}

Respectfully,
[Name, lot #, contact]
"""
    print(letter)


def cmd_fine(a) -> None:
    rule = STATE_RULES.get(a.state.upper(), STATE_RULES["OTHER"])
    problems = []
    if not a.hearing_held:
        problems.append("NO HEARING held before the fine became effective — "
                        "procedural defect, demand reversal")
    if a.repeat == "no" and a.fine > 150:
        problems.append(f"First-offense fine ${a.fine:.0f} is above the common "
                        "first-offense band ($25-150) — challenge reasonableness")
    if a.repeat == "yes" and a.fine > 1000:
        problems.append("Repeat fine exceeds the FL-style $1,000 aggregate band — "
                        "check your state's cap structure")
    verdict = "FINE IS VULNERABLE" if problems else "FINE LOOKS PROPERLY LEVIED — argue the merits"
    print(f"=== Fine review ({a.state}): ${a.fine:.0f} for {a.violation!r}")
    print(f"Statute frame: {rule['statute']}")
    print(f"Rule: {rule['fine_rule']}\n")
    for i, p in enumerate(problems, 1):
        print(f"  DEFECT {i}: {p}")
    print(f"\nVERDICT: {verdict}")
    if problems:
        print("\nNext step: written demand citing the defects above, request "
              "hearing, and reversal with refund. Keep certified-mail proof.")
    print("\nIf you must pay to avoid a lien: mark the check "
          "'paid under protest, pending hearing' and say so in writing.")


def cmd_assessments(a) -> None:
    print(f"=== Assessment projection: ${a.monthly:.0f}/mo growing {a.growth*100:.1f}%/yr\n")
    print(f"{'Year':<6}{'Monthly':>10}{'Annual':>11}{'Cumulative':>13}")
    total = 0.0
    m = a.monthly
    for y in range(1, a.years + 1):
        annual = m * 12
        total += annual
        print(f"{y:<6}{m:>10,.0f}{annual:>11,.0f}{total:>13,.0f}")
        m *= (1 + a.growth)
    flat_total = a.monthly * 12 * a.years
    print(f"\nGrowth premium vs flat: ${total - flat_total:,.0f} over {a.years} years")
    print("Use this at open forum: demand the reserve study funding plan and the "
          "board's inflation justification. Special assessments need the "
          "membership vote threshold in your bylaws (often a majority or "
          "supermajority of ALL owners) — ask for the vote record.")


def cmd_records(a) -> None:
    rule = STATE_RULES.get(a.state.upper(), STATE_RULES["OTHER"])
    print(f"""[Name / lot]
[Association] — Records Request under {rule['records']}

Please make the following official records available for inspection and
copying within the statutory period:
1. Annual budgets and any amendments, current fiscal year + prior 2 years.
2. Board meeting minutes and agendas, last 24 months.
3. Reserve study or reserve funding plan (most recent).
4. All management and vendor contracts in force.
5. The currently adopted fine/violation schedule with adoption date.
6. Delinquency/ receivables summary (redacted as required).
7. Insurance policies summary (master policy declarations).

I will pay statutory per-page copying costs for copies. Please confirm receipt
and the production date. If any record is withheld, please cite the specific
statutory exemption in writing.

[Name, lot #, date]""")


def run_demo() -> None:
    import types
    print("========== DEMO 1: violation response letter ==========")
    v = types.SimpleNamespace(violation="trash cans visible from street", fine=0,
                               deadline_days=14, state="CA", ccr="3.7 Trash Receptacles")
    cmd_violation(v)
    print("========== DEMO 2: hearingless fine review ==========")
    f = types.SimpleNamespace(fine=250, violation="fence stain color", repeat="no",
                              hearing_held=False, state="CA")
    cmd_fine(f)
    print("========== DEMO 3: assessment escalation ==========")
    a = types.SimpleNamespace(monthly=385, growth=0.07, years=10)
    cmd_assessments(a)
    print("========== DEMO 4: records demand (FL) ==========")
    r = types.SimpleNamespace(state="FL")
    cmd_records(r)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    pv = sub.add_parser("violation")
    pv.add_argument("--violation", required=True)
    pv.add_argument("--fine", type=float, default=0)
    pv.add_argument("--deadline-days", type=int, default=14)
    pv.add_argument("--state", default="OTHER")
    pv.add_argument("--ccr", default="[covenant § from the notice]")
    pf = sub.add_parser("fine")
    pf.add_argument("--fine", type=float, required=True)
    pf.add_argument("--violation", required=True)
    pf.add_argument("--repeat", choices=["yes", "no"], default="no")
    pf.add_argument("--hearing-held", type=bool, default=False)
    pf.add_argument("--state", default="OTHER")
    pa = sub.add_parser("assessments")
    pa.add_argument("--monthly", type=float, required=True)
    pa.add_argument("--growth", type=float, default=0.07)
    pa.add_argument("--years", type=int, default=10)
    pr = sub.add_parser("records")
    pr.add_argument("--state", default="OTHER")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        run_demo()
    elif a.cmd == "violation":
        cmd_violation(a)
    elif a.cmd == "fine":
        cmd_fine(a)
    elif a.cmd == "assessments":
        cmd_assessments(a)
    elif a.cmd == "records":
        cmd_records(a)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
