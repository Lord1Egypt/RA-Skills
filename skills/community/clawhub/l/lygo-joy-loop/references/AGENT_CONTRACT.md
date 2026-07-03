# Joy Loop — Agent contract (mandatory)

Read `SECURITY.md` first. Violations = stop and ask the user.

## When this skill may activate

Use **only** when the user clearly asks for one of:

- Running or debugging **Joy Loop** / **joy-loop-pulse** / **joy_loop_protocol** in the LYGO stack
- **Architect** dashboard or **122 BPM** council swarm tick (local)
- **Joy Loop kernel egg** plant (with consent)
- Lattice check involving **JoyLoopRegistry** or **joy_loop_snapshot**

Do **not** activate for generic “joy”, “lattice”, “council”, or “Δ9” chat with no stack task.

## Before any command

1. Confirm `LYGO_STACK_ROOT` (or cwd is stack root) with the user if ambiguous.
2. State **tier** (see SECURITY.md) and **files that will change**.
3. If snapshot may become public via push, **warn once per session**.

## Allowed without extra confirmation

- Explain docs, read snapshot/registry JSON, run `pytest tests/test_joy_loop_*.py` (no persist)

## Requires explicit user confirmation

- `--tick` (automated army is OK **only** if user previously enabled joy-loop-pulse)
- `--inject`, `--repl`, `--dashboard`, `--architect`, `--serve`
- Any plant or registry rebuild

## Forbidden unless user literally requests

- `git push`, `gh`, ClawHub publish, social posts
- Running plant without `--i-consent` and documented consent
- Pointing dashboard/API at `0.0.0.0` or tunneling without user ask

## Skill scripts

- `scripts/plant_joy_loop.py` — requires `LYGO_JOY_PLANT_CONSENT=yes`; does **not** imply consent by itself.

## Chain order

`lygo-protocol-stack-operator` → `lygo-kernel-egg-planter` (optional) → **`lygo-joy-loop`** → `lygo-ollama-army` (`joy-loop-pulse`)