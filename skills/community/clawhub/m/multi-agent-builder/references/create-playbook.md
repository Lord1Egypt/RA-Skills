# Create Playbook (Execution-Ready)

Use this after user confirms roles.

## Step 0: Confirmation gate (required)
Confirm with user:
- final role list

Do NOT ask user to confirm these internal steps; execute automatically:
1) openclaw.json agent materialization
2) A2A/subagents permission setup

If role list is not confirmed, stop and ask.

## Step 1: Agent ID normalization
Rules:
- lowercase letters, digits, hyphen only
- 2-24 chars
- stable semantic names (e.g., `product-manager`, `tech-architect`)
- avoid duplicates and reserved generic ids (`agent`, `assistant`, `bot`)

## Step 2: Per-agent contract
For each role, define:
- id
- mission
- deliverables
- dependencies
- escalation target

Ensure `team-leader` is present and designated as:
- single user-facing intake role
- stage transition controller
- final consolidation owner

## Step 3: Collaboration topology
Build adjacency list:
- who delegates to whom
- who reports to whom
- critical path roles

Prefer star-topology around `team-leader` for small teams (3-8 roles).

## Step 4: SOUL/AGENTS/IDENTITY materialization
Inject full role guidance:
- SOUL: role positioning, expert capability scope, responsibilities, boundaries, quality bar
- AGENTS: team directory, routing conventions, return-path rules, reporting rules
- IDENTITY: localized role display name (Chinese when user speaks Chinese, etc.)

Use templates from `snippet-templates.md` and role depth guidance from `role-soul-blueprints.md`.

## Step 5: Shared workspace initialization
Create team shared directory:
- `/workspace-<team>/shared/`
- all stage deliverables must be stored under this directory
- all team roles treat this as shared artifact hub

Enforce ownership rule:
- specialist roles write artifacts into shared/
- team-leader references paths and summaries only

## Step 6: Config materialization (openclaw.json) [AUTO]
Use `scripts/create_team.mjs` single entrypoint; do not run partial steps manually.
Materialization must include:
- create/update `agents.list[]` for all roles
- set `subagents.allowAgents` A2A boundaries
- create/update required `bindings[]`
- generate per-role files including AGENTS.md
- validate channel account consistency

This step is automatic and should not require user confirmation.
Use `config-materialization-checklist.md`.

## Step 7: Post-creation channel binding plan (single-bot only)
After team creation is complete:
- ask user to choose one channel for `team-leader` only
- ask user whether to **auto-bind now** or **skip and configure manually**
- if user chooses auto-bind: ask user to provide required credential/token, then perform binding
- if user chooses skip: provide exact manual config checklist and stop binding actions
- prompt user to run an activation test message after binding (auto or manual)

Rules:
- do not ask channel questions before creation
- do not bind specialist roles directly for default test/use path
- if required token fields are uncertain, check OpenClaw docs first, then ask user exactly those fields

## Step 8: Validation checklist
- all roles have measurable outputs
- all dependencies have return path
- escalation owner exists
- channel mapping complete
- config materialization checks all passed (agents/bindings/A2A)
- every role has non-placeholder SOUL.md/AGENTS.md/IDENTITY.md
- shared workspace exists at team root: `/workspace-<team>/shared/`
- no-raw-bulk-output rule is present in role docs

## Step 9: Handoff to user
Return:
- team creation report (mandatory)
- team roster
- flow
- stage deliverables + paths
- protocol summary
- security summary (skills checked + decisions)
- smoke test prompt

After report, append channel binding blueprints automatically.
