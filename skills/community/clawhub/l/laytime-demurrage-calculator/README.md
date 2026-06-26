# Laytime & Demurrage Calculator (Voyage Charter)

**Platforms:** Claude · Openclaw · Codex
**Domain:** Maritime / Chartering / Post-Fixture Operations

## Purpose

Turns a voyage-charter party, the port Statement of Facts (SoF), and the Notice of Readiness (NOR) tender/acceptance record into a clause-by-clause DRAFT laytime statement: a timesheet that applies the charter's exception regime hour-by-hour, a comparison of used vs allowed laytime, the resulting demurrage or despatch amount (full or half-despatch, where applicable), disputed-period flags, an evidence index that anchors every timesheet row to a specific SoF entry, and an open-questions list — for chartering, operations, claims-team, and counsel review before any invoice, counter-claim, or arbitration filing.

## When to Use

- A chartering / operations manager needs a post-fixture laytime statement on a single voyage (load port, discharge port, or both)
- A claims handler needs to draft a demurrage claim against a charterer or a counter-claim against an owner
- A port agent needs a defensible SoF-to-timesheet conversion before circulating to principals
- A trader / shipper needs to verify a freight-and-demurrage invoice received from a tonnage provider
- An owner or charterer is preparing a Reference to LMAA / SCMA / SMA arbitration on a laytime dispute and needs a clean computation to attach
- A bunker / port-cost analyst needs to test the demurrage exposure on a proposed fixture before owners sign the charter

## What It Does

**Phase 1: Charter, Voyage, and Port Intake**
1. Captures the charter party (form — Gencon, Asbatankvoy, Synacomex, NYPE-voyage, bespoke; addenda; rider clauses), the vessel, the cargo, the voyage (load / discharge ports), and the parties (owner / charterer / receiver / shipper / agent)
2. Extracts the laytime regime — laytime allowed (hours or days, per port or reversible/non-reversible), the demurrage rate (USD/day pro rata), the despatch rate (USD/day pro rata, full or half), the WWDSHEX / SHINC / SHEX / WWD / running hours convention, the exception clauses (strike, weather, ice, breakdown, "shifting from anchorage to berth not to count"), and the NOR provisions (when tenderable, to whom, in what form, working hours / "office hours")

**Phase 2: NOR Validity Walkthrough**
3. Tests each NOR against the charter's NOR clause: (a) tendered in writing per the charter (b) vessel in all respects ready (physical and legal readiness — free pratique, customs, holds clean and dry where required, tanks accepted) (c) at the agreed place (berth / anchorage / customary waiting place) (d) within the agreed hours (e) to the right party (charterer, receiver, agent)
4. Records each NOR tender (timestamp, channel, party, "in writing or message agreed by parties"), each acceptance / rejection / silence-treated-as-accepted, and computes the resulting laytime commencement per the charter's "NOR + turn time" provision (e.g. "WIBON, WIPON, WIFPON, NOR accepted = laytime to commence at 0600 next working day after tender")

**Phase 3: Timesheet Construction**
5. Builds the timesheet in defensible granularity (hour-by-hour for short stays, day-by-day for long stays), one row per event, anchored to the SoF
6. Applies exceptions clause-by-clause: weather-working-day deductions (with rain / wind / swell evidence), Sundays / Holidays In or Out (SHEX / SHINC) per the port-specific holiday calendar, strikes (with cause-and-effect test), breakdowns of vessel cranes (deducted) vs port cranes (charter-dependent), shifting time (counts unless excluded), "once on demurrage always on demurrage" override (after laytime is exhausted, only the carefully-drafted "fault of owner" exception interrupts the running of demurrage), interrupted laytime (work attempted but failed counts unless specifically excluded)

**Phase 4: Used vs Allowed and Computation**
7. Sums used laytime, compares to allowed laytime (per port if non-reversible, totalled if reversible / averaged where the charter so provides), produces "time on demurrage" or "time saved" with hours / minutes precision
8. Applies the demurrage or despatch formula — demurrage = time on demurrage × daily rate / 24, despatch = time saved × despatch rate / 24, with half-despatch (despatch rate = half the demurrage rate) where the charter says "DHD" or "half despatch on all time saved both ends"
9. Tests the charter for the alternative "all working time saved" vs "all time saved both ends" despatch base — the difference often doubles the despatch amount

**Phase 5: Statement, Evidence Index, and Disputed-Period Flags**
10. Produces a DRAFT laytime statement formatted for the recipient (owner ↔ charterer, charterer ↔ receiver), with the timesheet, the computation, the dollar amount payable (and to whom), and a covering memo that cites the operative charter clauses
11. Builds the evidence index — SoF, NOR tenders and acceptances, port log, vessel log, weather record, port circular and holiday calendar, surveyor / pilot reports, photographs, terminal correspondence — and cross-references every timesheet row
12. Lists disputed-period flags (e.g. "owner asserts WWDSHEX, charterer asserts SHINC for the period 0800-1800 Sunday — clause 6 controls — counsel to confirm") and an Open Questions list for any input the user marked unknown

## Output

A laytime packet consisting of a DRAFT laytime statement (with the timesheet, used-vs-allowed comparison, and the demurrage or despatch amount), a covering memo that cites the operative charter clauses, a numbered evidence index, a list of disputed-period flags, and an Open Questions list for any unresolved input — all marked **DRAFT — FOR CHARTERING / OPERATIONS / CLAIMS-TEAM AND COUNSEL REVIEW**.

## Notes

This skill **drafts** a laytime / demurrage / despatch computation to support — never replace — chartering, operations, claims-team, and counsel review. The skill does not issue an invoice, does not send a notice of claim, does not concede or waive a position on behalf of any principal, does not opine on the enforceability of any charter clause, and does not opine on arbitration outcomes. The skill follows the express words of the charter party first (charter trumps general principles), then the law / forum chosen by the charter (English law, U.S. law, Singapore law) only where the user supplies it — and where the user does not, the skill flags interpretive choices rather than assuming them. The skill applies to voyage charters by default; time-charter off-hire and trip-charter performance claims are out of scope and should be flagged for a future skill.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
