# OpenClaw Multi-Agent Wizard

A beginner-friendly Codex/OpenClaw skill that helps users create OpenClaw multi-agent setups step by step, with a strong focus on simple explanations, Feishu onboarding, and safe defaults.

## GitHub Description

Short repository description:

> A beginner-friendly OpenClaw multi-agent setup wizard for Codex, with safe Feishu onboarding and automatic starter profile generation.

Suggested first release tagline:

> Build OpenClaw multi-agent step by step, even if you do not understand the underlying configuration yet.

This skill is designed for users who do **not** already understand OpenClaw concepts like agents, bindings, routing, `chat_id`, or Feishu app setup. Instead of expecting users to know the platform, it acts like an installation wizard and guides them through one small decision at a time.

## What This Skill Does

This skill helps users:

- choose a beginner-friendly multi-agent mode
- create one or more OpenClaw agents
- generate starter role files for each agent automatically
- connect Feishu bots step by step
- configure beginner-safe routing
- verify setup and explain the final result in plain language

## Supported Modes

### 1. Multi-bot, multi-agent

One bot maps to one agent.

Example:

- work bot -> work assistant
- life bot -> life assistant

This is the safest and easiest default for beginners.

### 2. Single-bot, multi-agent

One Feishu bot is shared, but different Feishu groups map to different agents.

Example:

- product group -> product assistant
- engineering group -> engineering assistant

V1 supports **group-based routing only** for this mode.

### 3. A2A collaboration

One main agent talks publicly, while one or more worker agents help in the background.

Example:

- main assistant replies in Feishu
- data assistant gathers numbers
- writing assistant polishes the final response

For Feishu, the recommended default is:

- one public main agent
- background worker agents

## What Gets Generated for Each Agent

When the skill creates an agent, it does not leave the workspace empty.

It can automatically generate a starter profile bundle:

- `IDENTITY.md`
- `SOUL.md`
- `AGENTS.md`
- `MEMORY.md`
- `TOOLS.md`
- `USER.md`

This gives each new agent a lightweight default identity, role boundary, collaboration shape, memory focus, tool guidance, and user-facing purpose.

## Feishu Focus

This skill currently focuses on Feishu because it is one of the most practical OpenClaw onboarding paths for beginner users in this workflow.

The Feishu flow is intentionally broken into very small steps:

1. create a Feishu app
2. enable bot capability
3. copy `App ID` and `App Secret`
4. finish event subscription
5. connect OpenClaw
6. bind the bot or group routing
7. verify the result

If the user gets lost inside Feishu, the skill is designed to re-anchor on visible page titles and left-side menu labels instead of dumping raw documentation.

## Design Principles

This skill is intentionally conservative:

- preflight first
- one small step at a time
- safe defaults over many options
- one bot at a time
- one group at a time
- minimal config edits
- verify before claiming success

It is optimized for beginner success, not maximum feature coverage.

## Current Boundaries

This version intentionally does **not** treat every advanced OpenClaw feature as a beginner path.

Current boundaries:

- single-bot multi-agent supports Feishu **group** routing only
- private-chat routing is treated as advanced
- advanced runtime orchestration is explained carefully, not auto-enabled by default
- same-group public multi-agent chatter is treated as experimental, not as the recommended Feishu default

## Directory Structure

```text
openclaw-multi-agent-wizard/
├── SKILL.md
├── README.md
├── .gitignore
├── agents/
│   └── openai.yaml
├── assets/
│   ├── icon-small.svg
│   └── icon-large.svg
├── references/
│   ├── a2a-mode.md
│   ├── advanced-mode.md
│   ├── command-branches.md
│   ├── dialogue-scripts.md
│   ├── feishu-setup.md
│   ├── final-summary.md
│   ├── migration-existing-setup.md
│   ├── modes.md
│   ├── persona-templates.md
│   ├── preflight.md
│   ├── quick-start.md
│   ├── routing-basic.md
│   └── troubleshooting.md
└── scripts/
    ├── generate_agent_ids.py
    ├── render_setup_summary.py
    ├── suggest_persona_kind.py
    ├── write_identity_template.py
    └── write_starter_profile.py
```

## Key Files

- [SKILL.md](./SKILL.md): main skill instructions
- [agents/openai.yaml](./agents/openai.yaml): UI metadata
- [references/quick-start.md](./references/quick-start.md): compact mental model
- [references/feishu-setup.md](./references/feishu-setup.md): Feishu onboarding flow
- [references/persona-templates.md](./references/persona-templates.md): starter profile guidance
- [references/a2a-mode.md](./references/a2a-mode.md): A2A collaboration model
- [scripts/write_starter_profile.py](./scripts/write_starter_profile.py): starter profile bundle generator

## Installation

Place this skill where Codex can discover local skills.

Typical local skill location:

```text
$CODEX_HOME/skills/openclaw-multi-agent-wizard
```

If `CODEX_HOME` is not set, a common default is:

```text
~/.codex/skills/openclaw-multi-agent-wizard
```

## Validation

Validate the skill with the built-in skill validator:

```bash
python /path/to/quick_validate.py /path/to/openclaw-multi-agent-wizard
```

In this project, validation was repeatedly run with the skill-creator validator and the skill passed.

## Development Notes

This repository includes small helper scripts for deterministic setup behavior:

- `generate_agent_ids.py`: create safe agent IDs from display names
- `suggest_persona_kind.py`: guess a starter role category from the agent name
- `write_starter_profile.py`: generate the six-file starter profile bundle
- `render_setup_summary.py`: generate a beginner-friendly final summary

The older `write_identity_template.py` script is retained as a compatibility wrapper and now also writes the full starter profile bundle.

## Recommended Open Source Positioning

If you publish this on GitHub, a clear positioning sentence would be:

> A beginner-friendly OpenClaw multi-agent setup wizard for Codex, with safe Feishu onboarding, simple mode selection, and automatic starter profile generation for each agent.

## Future Improvements

Possible next steps:

- add more channel-specific onboarding paths beyond Feishu
- add optional deeper persona refinement after initial setup
- add stronger migration support for messy existing OpenClaw configs
- add more worker role categories for specialized A2A teams

## License

This project is released under the [MIT License](./LICENSE).
