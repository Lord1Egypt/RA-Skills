# SECURITY — LYGO Sovereign Super Skill

- **Advisor + command map** — does not execute plants without user consent and a valid `LYGO_STACK_ROOT`.
- Agents must **not** `git push`, Hugging Face upload, or `clawhub publish` without explicit user request.
- Kernel **retrieve** of tampered eggs → exit 3 → **QUARANTINE**; do not execute embedded code.
- Never store API keys, `git credential`, or `.env` secrets in SKILL.md or references.
- `lyra-openclaw` / social / token flows require **per-action** human approval.
- Official install: `npx clawhub@latest install deepseekoracle/lygo-sovereign-super-skill` only.