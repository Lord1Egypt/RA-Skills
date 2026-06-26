---
name: openclaw-saas-builder
description: Build SaaS projects end-to-end with OpenClaw as orchestrator and Gemini CLI as a local planning and generation copilot. Use when the user asks to brainstorm, define, scaffold, implement, document, create a GitHub repository, or optionally deploy a SaaS, web app, MVP, internal tool, landing page, dashboard, or productized automation. This skill coordinates requirements, architecture, Rules.md, project-specific skills or plans, implementation phases, GitHub CLI usage, and optional Vercel deployment.
---

# OpenClaw SaaS Builder

Use this skill when the user wants full project orchestration instead of a quick snippet.

## Core idea

OpenClaw is the driver.
Gemini CLI is the brainstorming and generation copilot.
GitHub CLI is for repo creation and GitHub operations.
Vercel CLI is optional for deployment.

Do not treat Gemini as an unsupervised executor.
Use it to generate plans, alternatives, code drafts, copy, architecture ideas, and reviews.
OpenClaw remains responsible for file edits, shell execution, validation, and external side effects.

## What this skill should produce

For a serious SaaS or web project, aim to create at least:
- `requirements.md`
- `architecture.md`
- `Rules.md`
- `README.md`
- `TODO.md`
- `skills-plan.md`
- source code scaffold or implementation

For deployment-ready work, also aim for:
- `.env.example`
- `deployment.md`
- CI/deploy notes

## Preflight first

Before promising repo creation or deployment, run the preflight helper:

```bash
./skills/openclaw-saas-builder/scripts/preflight_saas_builder.sh
```

Interpretation:
- If Gemini CLI fails, continue with OpenClaw-only planning or ask whether to proceed without Gemini.
- If `gh auth status` fails, do not promise automatic repo creation yet.
- If `vercel whoami` fails, do not promise deployment yet.

If Vercel is required, the user should already have the CLI installed and authenticated.
Typical checks:
```bash
which vercel
vercel --version
vercel whoami
```

## Build modes

Read `references/saas-build-modes.md` when deciding scope.
Use one of these modes explicitly:
- idea mode
- MVP mode
- production mode
- launch mode

## Default workflow

### Phase 1: Discovery and brainstorming

Clarify:
- product goal
- target users
- pain point
- MVP scope
- must-have features
- non-goals
- monetization or business purpose
- data and privacy concerns
- preferred stack or constraints

Use Gemini CLI to accelerate this phase.
Prefer structured output.
Good pattern:
- ask Gemini for a concise options list
- ask Gemini for tradeoffs
- ask Gemini for a JSON spec draft

### Phase 2: Requirements package

Create these docs early:
- `requirements.md`
- `architecture.md`
- `Rules.md`
- `skills-plan.md`
- `TODO.md`

Use the bundled helpers when useful:
```bash
./skills/openclaw-saas-builder/scripts/generate_requirements.sh <project-name> '<brief>'
./skills/openclaw-saas-builder/scripts/generate_architecture.sh <project-name> '<brief>'
./skills/openclaw-saas-builder/scripts/generate_rules.sh <project-name> '<brief>'
```

Read `references/saas-doc-templates.md` for the expected sections.

If the user asks for diagrams, generate Mermaid diagrams in markdown first.

### Phase 3: Implementation plan

Break work into small, ordered milestones.
Use `TODO.md` or a milestone list.
Good milestone pattern:
1. bootstrap repo
2. scaffold app
3. core domain logic
4. auth and data
5. UI and polish
6. tests
7. docs
8. repo publish
9. deploy

### Phase 4: Build

Choose the build path based on complexity.

#### For small or medium tasks
- inspect files directly
- use Gemini CLI for spec, code drafts, or review
- edit files with OpenClaw tools
- run tests locally

#### For larger coding tasks
Prefer ACP or coding-agent for implementation loops.
Use Gemini CLI as planning and review support, not as the only coding engine.

### Phase 5: GitHub repository creation

Only do this when the user has explicitly asked for it or clearly requested end-to-end setup.

Typical local flow:
1. initialize git if needed
2. create README and baseline docs
3. verify `gh auth status`
4. create repo with a sensible name
5. set remote
6. commit initial version
7. push default branch

Use the helper when appropriate:
```bash
./skills/openclaw-saas-builder/scripts/create_github_repo.sh <repo-name> [--private|--public]
```

Use the GitHub skill for detailed command patterns.

Naming guidance:
- use a short, readable slug
- prefer product name or function over vague names
- avoid joke names unless the user asks

### Phase 6: Optional Vercel deployment

Only do this when the user asked for deployment.

Before deploy, verify:
```bash
which vercel
vercel --version
vercel whoami
```

If Vercel auth is not ready, stop and say exactly that.
Do not fake deployment readiness.

Use the helper when appropriate:
```bash
./skills/openclaw-saas-builder/scripts/deploy_vercel.sh
```

Typical flow:
1. verify framework and build output
2. confirm env vars
3. run Vercel link or init if needed
4. deploy
5. capture deployment URL
6. write deploy notes to `deployment.md`

## Safety and approval rules

These actions change the outside world and should be treated as explicit-user-intent actions:
- creating remote repos
- pushing commits to remote
- creating cloud projects
- deploying to Vercel
- sending webhooks or emails

Planning, docs, scaffolding, and local implementation can proceed normally.
For external side effects, confirm intent if the request is ambiguous.

## How to use Gemini CLI inside this skill

Use `gemini-cli` skill patterns.
Recommended helpers:
- `./skills/gemini-cli/scripts/check_gemini.sh`
- `./skills/gemini-cli/scripts/gemini_json_validate.sh`
- `./skills/gemini-cli/scripts/gemini_review.sh`
- `./skills/gemini-cli/scripts/gemini_with_model.sh`

Recommended Gemini uses:
- brainstorming product directions
- generating JSON specs
- drafting architecture alternatives
- drafting landing-page copy
- reviewing rewritten files
- naming ideas for repos or products

Bad use:
- blindly executing Gemini-generated shell
- trusting invalid JSON
- letting Gemini decide external side effects without review

## Recommended outputs by project stage

### Early stage
- `requirements.md`
- `architecture.md`
- `Rules.md`
- `TODO.md`

### Mid stage
- code scaffold
- component and module plan
- `.env.example`
- test checklist

### Late stage
- `README.md`
- `deployment.md`
- GitHub repo
- deploy URL

## References

Read these when needed:
- `references/saas-doc-templates.md`
- `references/repo-and-deploy-checklist.md`
- `references/saas-build-modes.md`

Use `skills/gemini-cli/references/website-prompts.md` when the project includes a marketing site or landing page.

## Publish readiness notes

This skill is meant to be practical, not magical.
It assumes:
- Gemini CLI is installed and authenticated
- GitHub CLI is installed and authenticated for repo creation
- Vercel CLI is installed and authenticated for deployment
- OpenClaw remains the orchestrator for validation, editing, and safety decisions
