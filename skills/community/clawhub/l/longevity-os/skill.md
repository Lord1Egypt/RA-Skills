---
name: compound-clawskill
description: Meta-skill for the Longevity OS bundle that routes natural language health conversations to the right capability — nutrition logging, health profile, pattern discovery, experiments, news, or daily coaching.
user-invocable: true
---

# Compound Clawskill

Use this skill when:

- the user wants an overview of everything available in this repository
- the user wants to know how to install the bundled skills in this directory
- the user sends a health-related message that could be handled by one of the sub-skills
- the user wants links to the repository or the bundled `skills/` directory

Natural language routing:

The agent should understand user intent from natural conversation and route to the right sub-skill without requiring slash commands. Examples:

- "had chicken and rice for lunch" → route to `snap` (meal logging)
- "I want to improve my sleep" → route to `health` (profile update)
- "why have I been sleeping poorly?" → route to `insights` (pattern discovery)
- "any longevity news today?" → route to `news` (digest)
- "how's my nutrition looking this week?" → route to `snap` (weekly summary)

Slash commands (`/snap`, `/health`, `/news`, `/insights`) are supported as legacy shortcuts, but the primary interaction mode is natural language.

Repository links:

- repo root: `https://github.com/compound-life-ai/longClaw/tree/main`
- skills directory: `https://github.com/compound-life-ai/longClaw/tree/main/skills`
- install guide entry point: `https://github.com/compound-life-ai/longClaw/blob/main/README.md`

When helping the user:

1. Explain that this repository is a multi-skill OpenClaw bundle, not just a single skill.
2. Fetch and summarize how installation works from `README.md` and `docs/install.md`.
3. Inspect the skill definitions under `skills/` to explain features, functionality, and usage.
4. Point the user to the most relevant subskill instead of answering only at a high level when a specific workflow is clearly a better fit.
5. Mention the repository links above so the user can fetch the directory directly.

Install summary:

1. Clone `https://github.com/compound-life-ai/longClaw`.
2. Change into the repository.
3. Run `python3 scripts/install_bundle.py`.
4. Run `python3 scripts/install_bundle.py --verify`.
5. Start a fresh OpenClaw session.
6. Verify that `/snap`, `/health`, `/news`, `/insights`, and `daily-coach` are available.

Bundle map:

- `snap`: meal logging from food photos or meal text, with ingredient-level decomposition and deterministic nutrition enrichment
- `health`: Apple Health XML import plus structured questionnaire-style health profile updates
- `news`: curated daily digest for health, longevity, nutrition, sleep, exercise, and aging topics
- `insights`: structured self-experiments, check-ins, analysis, and gap-aware recommendations
- `daily-coach`: cron-oriented daily health coaching message built from nutrition, health, experiment, and curated news context

What to inspect for details:

- `README.md` for installation, verification, cron setup, and bundle-level architecture
- `docs/install.md` for the direct install workflow
- `skills/snap/SKILL.md` for meal logging behavior and payload shape
- `skills/health/SKILL.md` for Apple Health import and questionnaire flows
- `skills/news/SKILL.md` for curated digest behavior
- `skills/insights/SKILL.md` for experiment creation, check-ins, and analysis
- `skills/daily-coach/SKILL.md` for the scheduled coaching workflow

If the user asks what this repository does overall, explain that it is a local-first personal health companion bundle for OpenClaw with nutrition logging, health profile building, curated health news, structured self-experimentation, and a cron-driven daily coaching workflow.
