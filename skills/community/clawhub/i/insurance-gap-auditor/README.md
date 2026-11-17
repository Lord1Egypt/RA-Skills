# Insurance Gap Auditor

**Find out what your policies DON'T cover — before the claim does.**
15+ household loss scenarios (sewer backup, flood, e-bike, dog bite,
teen driver, wind deductible…) mapped to who pays and what's typically
excluded; the rider checklist that closes each gap with cost bands;
net-worth-based umbrella sizing; and a policy-inventory audit that
outputs the exact question list for your agent.

## The problem

People buy insurance in an afternoon and never audit it. The industry's
denial statistics have a pattern: flood ("I have home insurance"),
sewer backup ("that's water damage, right?"), the $2,000 jewelry
sub-limit on a $9,000 ring, the 2 % wind deductible nobody converted to
dollars. Every one of these is knowable in advance — but only if someone
walks your household's specifics against the standard exclusions, which
is exactly what agents do for wealthy clients and nobody does for
everyone else.

## What it does

- `scenarios` — loss event → which policy responds, the typical gap,
  and the exact question to ask.
- `exclusions` — standard gaps per policy type + closing riders with
  cost bands.
- `liability` — umbrella sizing from net worth + income.
- `policy add/list` — record what you carry.
- `audit` — cross-reference your inventory against the gap checklist:
  numbered, actionable output.

## Quick start

```bash
python3 scripts/insure_audit.py scenarios --group home
python3 scripts/insure_audit.py exclusions --policy home
python3 scripts/insure_audit.py liability --net-worth 450000 --income 95000
python3 scripts/insure_audit.py policy add --name "Home" --type home \
    --dwelling 380000 --liability 300000 --deductible 2500
python3 scripts/insure_audit.py audit --net-worth 450000
```

Stdlib-only Python 3. Data in a local JSON file.

## Who needs this

Every insured household. In the US alone that's ~250M people carrying
home/renters/auto policies they last read never. The audit takes 20
minutes a year and routinely finds five-figure gaps.

## Disclaimer

Educational tool encoding market-typical patterns (US personal lines,
UK/EU notes). Your contract and jurisdiction control — the output is
the question list, never a coverage opinion.

## License

MIT © 2026 Denis Voronin
