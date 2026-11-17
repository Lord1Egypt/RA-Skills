# Gift Occasion Planner

**Never again: the birthday you remembered the day after.**

Gift failure is a memory failure. Every year the same scramble — the
anniversary dinner booked nowhere, Mother's Day between playoff games, the
gas-station-flower bailout on the drive home. Expensive, obviously
last-minute, and quietly corrosive to the relationships it's supposed to
strengthen.

This is a gift intelligence system:

- **Registry** — people × occasions (birthdays auto-create; anniversaries,
  Mother's/Father's Day computed per year — they move, the tool knows)
- **60-day radar** — rolling lookahead with status per occasion:
  IDEA → BOUGHT → WRAPPED → GIVEN, and a ⚠ when an occasion inside 21 days
  still has nothing planned
- **Recommendation engine** — proposes gifts from profile ∩ history:
  never repeats (near-dupe detection), rotates interests and categories
  year over year, respects taboo lists, surfaces mentioned-wants first,
  fits budget ±20% — every suggestion carries its reasoning
- **Profiles that compound** — interests, sizes, taboo list, notes; year 3
  recommendations beat year 1's
- **Plan cards** — gift, budget, where to buy, buy-by date with shipping
  buffer, wrap-by date, card angle
- **Budget view** — the whole year's gift spend visible in March
- **ICS export** — 60/21/7/1-day reminders per occasion land in your real
  calendar with the profile summary embedded

100% local (`gifts.json`), pure stdlib Python.

## Quick Start

```bash
python3 scripts/gift_planner.py add-person "Mom" --birthday 1958-10-11 \
    --interests "gardening,opera,birdwatching" --taboo "no gadgets" --budget 75 \
    --notes "mentioned wanting better pruners"

python3 scripts/gift_planner.py radar          # next 60 days
python3 scripts/gift_planner.py recommend Mom  # 5 reasoned suggestions
python3 scripts/gift_planner.py plan birthday-2026 --idea "Felco pruners" --cost 68
python3 scripts/gift_planner.py status birthday-2026 --set bought
python3 scripts/gift_planner.py given birthday-2026 --gift "Felco pruners" --cost 68
python3 scripts/gift_planner.py budget
python3 scripts/gift_planner.py ics gifts.ics
```

## Example Radar

```
DUE IN 21 DAYS ──────────────────────────────
  Mom — BIRTHDAY (2026-10-11)
    Budget: $75.0   Status: IDEA   ⚠ NOTHING PLANNED
    Interests: gardening, opera, birdwatching
    Recent gifts: Felco pruners (2026); Bird feeder (2025)
    Suggestions:
      · class in opera ~$70    ← rotates away from gardening
      · botanical garden pass
```

## Who Needs This

Anyone with more than four important people — which is everyone. Especially:
large/blended families (15+ occasions/year), partners for whom anniversaries
are high-stakes, and anyone whose December credit-card statement is an
annual surprise.

## License

MIT — see [LICENSE](LICENSE).
