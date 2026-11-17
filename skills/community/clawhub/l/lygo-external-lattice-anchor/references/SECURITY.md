# Security — External Lattice Anchor (Layer C) v1.1.1

## Trust boundary

- Point `LYGO_STACK_ROOT` only at a **checkout you control**.  
- Untrusted stack roots can feed untrusted Python tools into allowlisted `runpy` paths under that root — treat stack as trusted code.  
- Public HTTPS is **mirror data**, not authority over local eggs.

## Protect the user

| Threat | Control |
|--------|---------|
| Malicious public mirror | Local A+B verify first; public is soft |
| Auto-exfil / auto-publish | Scripts never git push / HF upload / ClawHub |
| Poisoned chart growth | Star **proposals** only; steward gate + consent |
| Registry lag as tamper | Mismatch note “mirror lag”; not exit 3 |
| Shell injection | **No `os.system`**; no shell=True |
| Surprising mutation | Default verify = **zero writes** (v1.1.1) |
| Untrusted execute | `--build-manifest` / `--refresh-local` require `--i-trust-stack` |
| Manifest field abuse | `role`/`verify` enums; HTTPS-only URL; unknown verify → soft; role never dispatches |
| Skill supply chain | Install from `deepseekoracle`; LYGO Sovereign v2.0 |

## What runs by default (v1.1.1)

| Script | Network | Writes | Executes builders |
|--------|---------|--------|-------------------|
| `verify_public_anchors.py` | HTTPS GET | **none** | **no** |
| `verify_world_lattice.py` | via public verify | **none** | **no** |
| + `--write-report` | same | `tests/*_last_run.json` | no |
| + `--build-manifest --i-trust-stack` | same | may write docs/manifest | skill-local builder (runpy) |
| + `--refresh-local --i-trust-stack` | same | docs/manifest + proposals | skill-local builders (runpy) |
| `build_public_verify_manifest.py` | no | docs/manifest | n/a |
| `map_eggs_to_star_chart.py` | no | proposals JSON | n/a |
| `sync_external_plan.py` | no | none (dry) / snapshot with consent | n/a |

## Invocation model

- Skill scripts: `scripts/_safe_invoke.py` → `runpy.run_path` (allowlisted path)  
- A+B stack tool: `subprocess` list-argv, `shell=False`, `capture_output=True`  
- Argv rejects shell metacharacters  
- No `eval` / string `exec`  
- Endpoint `role` is **classification only** (never used for code routing)

## Network

- **HTTPS GET only** for verify  
- No credentials, cookies, or POST  

## Consent env

`LYGO_EXTERNAL_SYNC_CONSENT=yes` only for explicit snapshot execute (with `--execute-local-only`).
