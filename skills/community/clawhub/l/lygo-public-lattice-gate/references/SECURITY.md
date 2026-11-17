# Security — LYGO Public Lattice Gate v1.0.0

## Trust boundary

- Public HTTPS responses are **mirrors**, not authority over a local stack.  
- Optional `LYGO_STACK_ROOT` must be a checkout **you** trust.  
- This skill does **not** execute arbitrary code from the network.

## Protect the user / agent host

| Threat | Control |
|--------|---------|
| Auto-publish | Never git / HF / ClawHub / social |
| Live chart spam | Propose is dry-run only; no submit API |
| Shell injection | No `subprocess`, no `os.system`, no shell |
| Surprising writes | Default zero writes; opt-in `--write-report` / propose `--write` |
| Path escape | Reject `..` in write paths |
| Credential theft | No cookies, no POST, no API keys |
| SSRF | Fixed HTTPS endpoint list only (not user-controlled URLs) |

## Network

- **HTTPS GET only** to allowlisted LYGO public URLs  
- User-Agent identifies skill; no auth headers  

## Consent

- `--i-consent` on `propose` records intent only  
- Live Star Chart writes require **separate** skill + explicit human approval  

## Operator checklist

1. `python scripts/self_check.py`  
2. `python scripts/gate_cli.py verify`  
3. Read restore card before sharing digests externally  
4. Never paste private vault paths into proposals  

**Δ9Φ963**
