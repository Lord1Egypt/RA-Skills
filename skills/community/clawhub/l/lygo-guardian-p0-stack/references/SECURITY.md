# Security — lygo-guardian-p0-stack

## Scope

| In scope | Out of scope |
|----------|----------------|
| Text/content validation via bundled `src/guardian/` | Full P0–P9 deploy, publish, vault, deadman seeds |
| Optional read of **one user-specified file** ≤8192 bytes for gate | Scanning drives, env harvesting, external paths |
| `LYGO_STACK_ROOT` subprocess to **known** `lygo_p0_gate.py` | Arbitrary shell |

## Agent rules

1. **Default:** advise + `validate_decision` on pasted content — do not auto-run on whole disk.
2. **`isolate` / hard block** → do not send content externally; summarize risk to user.
3. **Not equivalent** to production Φ-gate — disclose when auditing bytes or skills for compliance.
4. No network in bundled scripts. No secrets in skill package.
5. Pair with **P0-gate unknown skills** before ingesting third-party SKILL.md into memory.

## Install notice

For **full lattice** install `lygo-protocol-stack-operator` separately with user review. This skill is a **lightweight guard**, not stack root access.