# Security — LYGO Geodesic Sealer v1.0.0

## Trust boundary

- Local `LYGO_STACK_ROOT` must be a checkout **you** trust.  
- Public HTTPS digests are **mirrors**, not authority over local seals.  
- This skill does **not** execute code from the network.  
- Software attestation is **not** a TPM quote — pair with stack `protocol6_quantum_attest` for hardware paths.

## Protect the user / agent host

| Threat | Control |
|--------|---------|
| Auto-publish | Never git / HF / ClawHub / social |
| Live chart spam | No Star Chart write APIs |
| Shell injection | No `subprocess`, no `os.system`, no shell |
| Surprising writes | Default zero writes; opt-in `--write` + `--i-consent` |
| Path escape | Reject `..` in write paths |
| SSRF | Fixed HTTPS dual-ledger list only (not user URLs) |
| Collapse / false certainty | Refuse lock when Truth or Chaos amp ~0 unless `--allow-collapse` |
| Credential theft | No cookies, no POST, no API keys |

## Network

- **Off by default**  
- `--network` enables **HTTPS GET only** to allowlisted dual-ledger URLs  
- User-Agent identifies skill; no auth headers  

## Consent

- `--i-consent` required for any filesystem write of seal artifacts  
- Human remains the only publisher  

## Operator checklist

1. `python scripts/self_check.py`  
2. `python scripts/seal_cli.py status`  
3. `python scripts/seal_cli.py attest --node-id <id> --truth ... --chaos ...`  
4. `python scripts/seal_cli.py verify --from-file <artifact>`  
5. Never paste private vault secrets into truth/chaos payloads  

**Δ9Φ963**
