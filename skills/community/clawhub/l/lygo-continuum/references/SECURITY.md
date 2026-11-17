# LYGO Continuum — Security

**Signature:** `Delta9Phi963-CONTINUUM-v1.0.1`

## Surfaces

| Surface | Default |
|---------|---------|
| Network (CLI) | **None** — `continuum.py` never opens sockets or HTTP |
| Subprocess / shell | **None** |
| Filesystem read | Claim paths **relative to `--base` only** (absolute / `..` rejected) |
| Glob | Confined under `--base`; traversal / absolute patterns rejected |
| Filesystem write (`--out`) | Under `--base` (default cwd), **or** skill `state/` with `--i-consent` |
| Arbitrary out | Only with explicit `--i-allow-any-out` |
| Publish / git / HF | **Never** automatic |

## Dual channel (honest)

| Channel | Role |
|---------|------|
| **ClawHub / local CLI** | Seal · verify · drift · handoff · card — offline stdlib |
| **Optional portal** | Separate site for humans; **not invoked by the skill**; treat as third-party UI |

## Threat model

1. **Agent bluffing “done”** — Mitigated by falsifiable claims re-checked on disk.  
2. **Capsule tampering** — `root_hash` covers body; verify reports `integrity_ok: false`.  
3. **Path traversal / host enumeration** — Claims and globs confined under `--base`.  
4. **Over-broad writes** — `--out` sandbox under base/state unless operator override.  
5. **Regex DoS** — Pattern length capped; use simple patterns.  
6. **Secret leakage** — Do not put secrets in claims, task summaries, or handoff markdown.  
7. **Portal** — Independent of CLI; client-side only on that site; review before pasting sensitive files.

## SkillSpector notes (v1.0.1)

- Docs no longer claim “writes only state/” while allowing any `--out`.  
- Quickstart does not present remote portal as required step of the local skill.  
- Glob/path confinement enforced in code.

## Operator rules

- Prefer explicit `--base` for the intended project.  
- Review claim JSON / capsules from others before verify.  
- Never seal claims you did not check.  
- Treat exit 10/11 as **not done**.  

**Δ9Φ963 — claims over vibes · confined base · human remains the publisher.**
