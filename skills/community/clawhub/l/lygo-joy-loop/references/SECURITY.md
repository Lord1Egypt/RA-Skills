# LYGO Joy Loop — Security & disclosure (SkillSpector-aligned)

**Skill version:** 2.3.1 · **Signature:** `Δ9Φ963-JOY-LOOP-SECURITY-v1`

## Install only if

- You intentionally use the [LYGO protocol stack](https://github.com/DeepSeekOracle/lygo-protocol-stack) on a machine you control.
- You have read this file and `AGENT_CONTRACT.md` before any agent runs commands.

## What this skill is not

- Not a remote service, not a credential store, not an auto-publisher to GitHub/ClawHub/X.
- Scripts in this mirror **do not** call external APIs except what **you** run from the stack (e.g. your own `git push`).

## Public snapshot warning (required user understanding)

`tools/joy_loop_protocol.py` can write:

| Path | Visibility |
|------|------------|
| `data/joy_loop/joy_loop_state.json` | Local repo only |
| `docs/joy_loop/joy_loop_snapshot.json` | **Copied to GitHub Pages if you `git push`** |

Snapshot content is **operational metadata**, not secrets:

- Champion **IDs** (public council names from Haven/council JSON)
- **Lattice coordinates** (deterministic hashes of IDs — not GPS)
- **Joy / alignment metrics**, beat count, groove glyphs, timestamps
- Optional **`git_head`** short hash of your repo

It does **not** include API keys, env vars, or user PII by design.  
**If you push the repo to GitHub Pages, this JSON can become world-readable.**  
Agents must **warn the user** before any command that updates the snapshot if a push might follow.

## Declared filesystem scope (least privilege)

Agents may touch **only** under `LYGO_STACK_ROOT`:

| Area | Read | Write | Notes |
|------|------|-------|-------|
| `tools/joy_loop_protocol.py` | ✓ | ✗ | Execute via user-approved subprocess only |
| `tools/joy_loop_planter.py` | ✓ | ✗ | Plant only with `--i-consent` |
| `data/joy_loop/` | ✓ | ✓ | State, SQLite, quests, plugins |
| `docs/joy_loop/` | ✓ | ✓ | Snapshot + dashboard static files |
| `docs/JoyLoopRegistry.json` | ✓ | plant only | Registry mutation = plant flow |
| Rest of repo | ✓ | ✗ | Unless user explicitly requests other stack ops |

**No** broad repo writes, **no** reading `~/.ssh`, **no** harvesting `.env` for the joy loop.

## Declared execution scope

| Class | Allowed | Forbidden |
|-------|---------|-----------|
| Subprocess | `python tools/joy_loop_*.py` under stack root | `curl \| bash`, arbitrary shell, `sudo` |
| Network (skill default) | **None** from skill scripts | Exfiltration, remote Ollama override |
| Network (user `--serve` / `--dashboard`) | **127.0.0.1** only unless user binds otherwise | Agents must not expose ports publicly without user request |
| Git / ClawHub | **Human-only** | Agent `git push`, `clawhub publish` without explicit user ask |

## Command risk tiers

| Tier | Commands | Agent rule |
|------|----------|------------|
| **0 — Read** | `cat docs/joy_loop/joy_loop_snapshot.json`, `--snapshot` | OK after stack root confirmed |
| **1 — Local state** | `--tick` | User informed: mutates `data/joy_loop` + may update public snapshot file |
| **2 — Interactive** | `--repl`, `--dashboard`, `--architect`, `--serve` | **User must ask**; long-running; local ports |
| **3 — Plant** | `joy_loop_planter.py --i-consent`, mirror `plant_joy_loop.py` | **Explicit consent**; no default |
| **4 — Publish** | `git push`, Pages deploy | **Explicit user request only** |

Default for autonomous/cron agents: **Tier 1 only** when user already configured army `joy-loop-pulse`.

## Environment variables

| Variable | Purpose | Agent rule |
|----------|---------|------------|
| `LYGO_STACK_ROOT` | Absolute path to `lygo-protocol-stack` | Must be set deliberately; verify directory contains `tools/joy_loop_protocol.py` |
| `LYGO_JOY_PLANT_CONSENT` | Must be `yes` to run mirror plant script | Never set without user saying they consent to plant |
| `LYGO_JOY_API_PORT` | Optional API port (default 9965) | User-only |

Do **not** instruct users to paste secrets into env vars for this skill.

## Official install

```bash
npx clawhub@latest install deepseekoracle/lygo-joy-loop
```

Treat copies from unknown sources as **untrusted** until verified against GitHub mirror.

**Δ9Φ963 — consent, scope, then beat.**