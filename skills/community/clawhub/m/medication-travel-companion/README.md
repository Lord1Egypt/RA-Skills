# Medication Travel Companion

**Flying with prescription medications without gambling at the border.**

Every year travelers lose medication, miss doses, or get arrested because of
rules they never knew applied: a legal Adderall prescription is a narcotics
offense in Japan; insulin dies in a frozen cargo hold; a controlled substance
in an unlabeled organizer can be confiscated anywhere. This skill screens your
actual med list before you fly.

## What it does

- **Screens each medication** against: US controlled-substance schedule,
  destination import bans (Japan, UAE, Singapore, China, Greece, ...), cold-chain
  stability windows (insulin 28-day in-use rule, GLP-1 pens, biologics),
  liquid/injectable carry-on rules, and supply math (pills needed vs on hand).
- **Builds a timezone-shift dosing plan** per regimen type (once daily, twice
  daily, basal insulin, fixed-interval birth control) with safe interval floors
  and a never-double rule.
- **Generates the doctor-letter request** with every required element and a
  ready-to-send email draft.
- **Prints a packing protocol**: rule-of-two supply splitting, Frio/gel-pack
  cold chain, hotel-fridge freeze warning, declaration script for screening.

## Real-world problem it solves

- ~1 in 2 adults takes a prescription drug; tens of millions fly with them.
- Stimulant prescriptions (ADHD) are effectively **banned** in Japan/UAE/China —
  travelers are detained annually over this exact scenario.
- Insulin + checked luggage = destroyed $300+ of medicine and a medical crisis
  abroad.
- Timezone dosing errors (doubling after a long-haul) are a classic ER visit.

## Usage

```bash
python3 scripts/medtravel.py screen \
  --meds "Adderall 20mg 2x daily; Lantus insulin 100u/mL" \
  --days 14 --destination japan --pills-on-hand 10

python3 scripts/medtravel.py schedule --med "metformin 2x daily" --from-tz 2 --to-tz -5
python3 scripts/medtravel.py letter --meds "Adderall 20mg; Lantus" --days 14
python3 scripts/medtravel.py packing --cold-chain --controlled --days 14
```

Full rule book: `references/medication-travel-rules.md`.

## Limits

Offline knowledge base, deliberately conservative: unknown drugs or countries
return a "verify with the embassy/pharmacist" verdict instead of a guess.
Not medical advice — doses stay exactly as prescribed.

## License

MIT © 2026 Denis Voronin
