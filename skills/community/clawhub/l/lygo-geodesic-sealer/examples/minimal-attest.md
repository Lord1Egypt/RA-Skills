# Minimal P6 geodesic attest

```bash
export LYGO_STACK_ROOT=/path/to/lygo-protocol-stack   # optional local ledgers

python scripts/self_check.py

python scripts/seal_cli.py attest \
  --node-id lattice-node-01 \
  --truth "dual-ledger-truth-anchor" \
  --chaos "creative-chaos-channel" \
  --nodes lattice-node-01,peer-alpha \
  --network

# Persist only with consent:
python scripts/seal_cli.py attest \
  --node-id lattice-node-01 \
  --truth "dual-ledger-truth-anchor" \
  --chaos "creative-chaos-channel" \
  --write ./attest-lattice-node-01.json \
  --i-consent

python scripts/seal_cli.py verify --from-file ./attest-lattice-node-01.json
```
