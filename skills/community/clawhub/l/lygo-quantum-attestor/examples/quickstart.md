# Quantum Attestor quickstart

```bash
python scripts/attestor_cli.py demo

python scripts/attestor_cli.py attest \
  --node-id lightfather \
  --truth "Eternal Truth" \
  --chaos "Creative Chaos" \
  --write ./attest.json --i-consent

python scripts/attestor_cli.py seal-delta9 \
  --from-file ./attest.json \
  --write ./sealed.json --i-consent

python scripts/attestor_cli.py verify-node --from-file ./sealed.json

python scripts/attestor_cli.py emit-receipt \
  --from-file ./sealed.json \
  --write ./receipt.json --i-consent
```

Then pair `receipt.json` with `lygo-continuum-integrator` / `lygo-mint-verifier`.
