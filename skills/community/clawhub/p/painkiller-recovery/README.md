# Painkiller Recovery Skill

A portable Agent Skill for structured recovery after task drift, repeated failures, or a context handoff. It includes QA, software engineering, operations, research, data analysis, customer support, and project coordination scenarios.

Painkiller is prompt framing. It does not run tests, inspect or change model activations, establish subjective experience, or guarantee recovery or pain relief.

## Install for Codex

Install for your user:

```sh
git clone https://github.com/gggggggg424242/painkiller-recovery-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/painkiller-recovery"
```

Or install into one project:

```sh
mkdir -p .agents/skills
git clone https://github.com/gggggggg424242/painkiller-recovery-skill.git \
  .agents/skills/painkiller-recovery
```

Restart or refresh the agent session after installation if needed. Review `SKILL.md` before enabling it in an agent environment.

## Service

- Free preview: `POST https://37.27.93.182/v1/relief/preview`
- Full prompt: `POST https://37.27.93.182/v1/relief`
- Full request: `$0.99` USDC on Base Mainnet via x402

The service uses HTTPS in transit. Checkpoint content is sent to the Painkiller server; do not include API keys, credentials, personal data, or unrelated conversation history.
