# What to Back Up

Use this inventory to decide what belongs in an OpenClaw recovery plan.

## Operational archive (safe for cloud/private GitHub storage)

| Path | Included by default | Why it matters | If you lose it |
|---|---:|---|---|
| `$HOME/.openclaw/workspace/` | Yes | Core agent memory, prompts, notes, local scripts, custom skills, active artifacts | You lose the agent's working brain and custom operating context |
| `$HOME/.openclaw/workspace/SOUL.md` | Via `workspace/` | Identity, tone, and operator behavior | The agent still runs but loses persona and behavioral nuance |
| `$HOME/.openclaw/workspace/MEMORY.md` | Via `workspace/` | Durable long-term memory | You lose curated memory and preferences |
| `$HOME/.openclaw/workspace/AGENTS.md` | Via `workspace/` | Operating rules, delegation model, and safety workflow | Orchestration quality drops and guardrails may be missing |
| `$HOME/.openclaw/workspace/memory/` | Via `workspace/` | Daily logs, bank files, blockers, and deep context | History and continuity disappear |
| `$HOME/.openclaw/workspace/scripts/` | Via `workspace/` | Local automation and repair tooling | Manual rebuild of workflows and helper scripts |
| `$HOME/.openclaw/workspace/skills/` | Via `workspace/` | Installed and custom skills | You lose custom packaged capabilities |
| `$HOME/.openclaw/openclaw.json` | Yes, redacted | Main OpenClaw configuration without embedded secrets | The node may start with wrong defaults or fail to match prior behavior |
| `$HOME/.openclaw/cron/jobs.json` | Yes | Scheduled automations and recurring tasks | All recurring jobs vanish |

## Encrypted secrets archive (local recovery only by default)

| Path | Included by default | Why it matters | If you lose it |
|---|---:|---|---|
| `$HOME/.openclaw/.env` | No — opt in via `--include-secrets` | Secrets, API keys, credentials, local overrides | External integrations may fail until secrets are rebuilt |
| `$HOME/.openclaw/agents/` | No — opt in via `--include-secrets` | Local auth profiles and agent-specific credentials/state | Re-authentication and local agent setup may be required |

## Not included

| Path | Included by default | Why it matters | If you lose it |
|---|---:|---|---|
| Local model cache / Ollama data | No | Downloaded model weights and local runtime state | Re-download required; backup size stays sane |
| `.git/` repos inside workspace | Indirect if under `workspace/` | History for custom projects | Without it, rollback and provenance are harder |
| Large caches, `node_modules`, temp files | Indirectly possible under workspace | Rebuildable bulk data | Usually safe to regenerate; excluding them manually keeps backups smaller |
| OS keychains / Secure Enclave data | No | Hardware-bound secrets | Must be recreated or exported through the OS-native tooling |

## Recommendation

1. Always back up `workspace/`, redacted `openclaw.json`, and `cron/jobs.json`.
2. Include secrets only when you truly need full disaster recovery.
3. Encrypt secrets client-side with `age` before they leave the machine.
4. Treat the operational archive as shareable with a private cloud repo; treat the secrets archive as local-sensitive by default.
