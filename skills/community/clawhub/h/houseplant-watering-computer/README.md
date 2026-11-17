# Houseplant Watering Computer

**"Water weekly" is why houseplants die. The right answer is how fast THIS
pot dries out — and that's physics, not folklore.**

Overwatering-driven root rot is the #1 houseplant killer. Plant apps and
care cards give calendar intervals that ignore everything that matters:
pot volume, substrate, light, temperature, humidity. This skill computes
the actual soil water balance per pot and returns the usable reservoir in
mL, the expected dryout time in days, the dose per watering, and a
check-before-watering rhythm. It also routes symptoms (the wet-wilting
trap, fungus gnats, brown tips) to the right diagnosis, and sizes wick/
self-watering reservoirs for vacations.

## Quick start

```bash
python3 scripts/watering_computer.py compute --substrate peat-mix \
  --pot-tapered 24,18,22 --plant large-foliage --light bright-indirect \
  --temp 22 --humidity 45
# → reservoir ~2.0 L, dose ~1.4 L, dryout ~5-6 days (summer), ~11 in winter

python3 scripts/watering_computer.py symptoms --soil wet --yellowing lower --gnats
python3 scripts/watering_computer.py check --finger-depth shallow --feels dry --pot-tapered 24,18,22
python3 scripts/watering_computer.py selfwatering --pot-tapered 24,18,22 --substrate peat-mix --away-days 21
```

Stdlib-only Python 3. Offline.

## What's inside

- `scripts/watering_computer.py` — compute / check / symptoms / selfwatering
- `references/water-balance.md` — WHC tables, pot geometry, VPD (Tetens),
  demand classes, dose derivation, wick engineering
- `references/symptom-router.md` — wet-vs-dry master table, gnat protocol,
  root-rot rescue stages, salt flush

## License

MIT © Denis Voronin
