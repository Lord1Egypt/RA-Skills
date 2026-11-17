# Mattress Spec Decoder

**The same mattress is sold under a different name at every retailer — on
purpose, so you can't compare prices. The spec sheet is the fingerprint.**

You will spend ~3,000 hours on this object in the next 8 years. The buying
decision is made almost impossible by design: exclusive model names,
marketing foam names ("UltraCool Gel Infinity"), 10-year warranties with 1.5"
sag loopholes, and firmness scales that mean nothing across brands.

This skill turns that into engineering:

- **`recommend`** — your firmness band (1–10) computed from sleep position +
  BMI, with target ILD range, mattress-type candidates, and hard requirements
  for heavier bodies (base foam ≥ 1.8 lb/ft³ etc.).
- **`decode`** — score any spec sheet: memory/base foam density bands, coil
  count vs type, expected lifespan, and which specs are pure marketing.
- **`couple`** — two-body compromise: shared core firmness + topper strategy,
  never the average.
- **`compare`** — two mattresses scored for YOUR profile with per-criterion
  reasoning and cost-per-good-year.
- **`warranty` / `sag`** — decode the 1.5" no-load loophole and prorated
  schedules; get a verdict on your measured dip.

## The real problem

- People replace mattresses every 8–10 years having used firmness scales and
  brand loyalty — the two variables with the least predictive value.
- Low-density base foam (the layer nobody advertises) is the #1 cause of
  "my mattress sagged after 2 years."
- Warranty claims fail on measurement protocol, not on defect absence.

## Quick start

```bash
python3 scripts/mattress_advisor.py recommend --position side --weight 78 --height 175
python3 scripts/mattress_advisor.py decode --type hybrid --memory-density 3.0 --base-density 1.5 --coils 480 --coil-type pocketed
python3 scripts/mattress_advisor.py couple --p1 side,62,168 --p2 stomach,95,182
python3 scripts/mattress_advisor.py compare --profile side,78,175 \
  --a 'name=CloudLux,type=hybrid,memory_density=4.0,base_density=1.8,coils=850,coil_type=pocketed,price=1100' \
  --b 'name=BoxFoam,type=foam,memory_density=2.5,base_density=1.3,price=500'
```

Stdlib-only Python 3. Offline. No brand affiliations.

## Repository layout

- `SKILL.md` — trigger conditions, workflow, pitfalls
- `references/mattress-science.md` — density/ILD/coil/latex deep dive, heat,
  off-gassing, lifespan tables
- `references/buying-playbook.md` — same-bed fingerprinting, negotiation,
  delivery inspection, warranty claims, topper rescue
- `scripts/mattress_advisor.py` — the decoder

## License

MIT © Denis Voronin
