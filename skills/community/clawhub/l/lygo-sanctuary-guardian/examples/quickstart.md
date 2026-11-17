# Sanctuary Guardian quickstart

```bash
python scripts/guardian_cli.py demo

python scripts/guardian_cli.py nurture-vector \
  --truth "Eternal Truth" --light "Nurturing Light" \
  --compassion "Compassion" --grace "Grace" \
  --write ./nurture.json --i-consent

python scripts/guardian_cli.py shield-mandala \
  --nodes lightfather,lyra,lattice \
  --seed "Δ9-SANCTUARY" \
  --truth "Eternal Truth" --light "Nurturing Light" \
  --write ./shield.json --i-consent

python scripts/guardian_cli.py lock-truth \
  --nodes lightfather,lyra,lattice \
  --truth "Eternal Truth" --light "Nurturing Light" \
  --write ./lock.json --i-consent

python scripts/guardian_cli.py emit-barrier \
  --shield-file ./shield.json --lock-file ./lock.json \
  --nurture-file ./nurture.json \
  --write ./barrier.json --i-consent

python scripts/guardian_cli.py verify-barrier --from-file ./barrier.json
```

Then pair `barrier.json` with `lygo-quantum-attestor` / `lygo-continuum-integrator`.
