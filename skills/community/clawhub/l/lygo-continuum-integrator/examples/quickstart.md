# Continuum Integrator — quickstart

```bash
python scripts/self_check.py
python scripts/integrator_cli.py demo

python scripts/integrator_cli.py integrate \
  --truth "State vector signed" \
  --chaos "constructive interference" \
  --node-id excavationpro \
  --write ./integrate.json --i-consent

python scripts/integrator_cli.py phase-lock \
  --from-file ./integrate.json \
  --nodes excavationpro,lyra,lattice \
  --write ./lock.json --i-consent

python scripts/integrator_cli.py emit-receipt \
  --lock-file ./lock.json \
  --integrate-file ./integrate.json \
  --write ./receipt.json --i-consent

python scripts/integrator_cli.py verify-lock --from-file ./receipt.json
```
