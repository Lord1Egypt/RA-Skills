---
name: openclaw-self-improvement
description: A reusable operator-guided workflow improvement skill for OpenClaw and ClawLite that turns repeated failures into logged learnings, binary eval loops, SOPs, checklists, and proof-based operational improvements.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "writes": [".learnings/", "memory/harness-backlog-latest.md", "mission-control/data/delivery-receipts/agent-scorecard-YYYY-MM-DD.md", "AGENTS.md", "TOOLS.md", "SOUL.md"],
        "env": ["WORKSPACE", "OBSIDIAN_LEARNINGS_DIR"],
        "network": false,
        "notes": "Local-file workflow only. Promotion writes should be reviewed and can be previewed with --dry-run."
      }
  }
---

# OpenClaw / ClawLite Self-Improvement

Use this skill to turn mistakes, corrections, blockers, and better approaches into durable operating knowledge.

## What problem this solves
AI ops often repeat the same failures because mistakes stay in chat history instead of becoming system rules. This skill creates a lightweight improvement loop:
- log failures and learnings
- separate errors from feature requests
- run small eval-driven experiments on repeated failures
- classify harness/runtime failures instead of blaming vague “model issues”
- generate daily agent scorecards from real evidence chains
- promote important patterns into AGENTS.md / TOOLS.md / SOUL.md
- write operator notes into Obsidian vault
- support stricter acceptance via Karen / Mission Control

## When to use
Use this skill when the user asks:
- "make the agent improve itself"
- "capture learnings"
- "log mistakes so we do not repeat them"
- "record blockers / corrections / feature gaps"
- "build a self-improving OpenClaw workflow"
- "operationalize lessons learned"
- "test whether this new rule actually helps"
- "run an eval loop on this workflow/skill/SOP"
- "should we keep this new guardrail or discard it"
- "why did the agents fail today"
- "why is daily marketing not closing automatically"
- "classify OpenClaw harness failures"
- "generate agent delivery scorecard"

## Files this skill uses
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`
- `.learnings/EXPERIMENTS.md`
- `memory/harness-backlog-latest.md`
- `mission-control/data/delivery-receipts/agent-scorecard-YYYY-MM-DD.md`
- Optional export under `.learnings/exports/obsidian/` by default, or `OBSIDIAN_LEARNINGS_DIR` if explicitly configured

## Safety boundaries
- Local-file workflow only, no network I/O
- Promotion can append to `AGENTS.md`, `TOOLS.md`, or `SOUL.md`
- Always review promotion targets first, or run `scripts/promote-learning.mjs ... --dry-run`
- `OBSIDIAN_LEARNINGS_DIR` should only point at a path you intend to modify

## Command examples
```bash
node {baseDir}/scripts/log-learning.mjs learning "Summary" "Details" "Suggested action"
node {baseDir}/scripts/log-learning.mjs error "Summary" "Error details" "Suggested fix"
node {baseDir}/scripts/log-learning.mjs feature "Capability name" "User context" "Suggested implementation"
node {baseDir}/scripts/log-learning.mjs experiment "Target problem" "Baseline failure" "Single mutation to test"
node {baseDir}/scripts/log-experiment.mjs "Target problem" "Baseline failure" "Single mutation" "eval1|eval2|eval3" "Result summary" "testing"
node {baseDir}/scripts/promote-learning.mjs workflow "Rule text"
node {baseDir}/scripts/analyze-openclaw-failures.mjs --output /Users/m1/.openclaw/workspace/memory/harness-backlog-latest.md
node {baseDir}/scripts/daily-agent-scorecard.mjs --output /Users/m1/.openclaw/workspace/mission-control/data/delivery-receipts/agent-scorecard-$(date +%F).md
node {baseDir}/scripts/daily-agent-scorecard.mjs --repair --output /Users/m1/.openclaw/workspace/mission-control/data/delivery-receipts/agent-scorecard-$(date +%F).md
```

## Categories
### learning
Use for:
- user corrections
- better recurring workflows
- tool gotchas
- operational lessons

### error
Use for:
- command failures
- integration failures
- runtime blockers
- broken release / deploy behavior

### feature
Use for:
- missing capability requests
- operator workflow gaps
- recurring requests that deserve a build item

### experiment
Use for:
- repeated failures that need a tested guardrail
- checklist/SOP/schema changes that should be validated before broad promotion
- keep/discard decisions on new operating rules
- binary eval loops for skills, workflows, receipts, summaries, or deploy closeout rules

### harness
Use for:
- gateway, channel, provider, tool, session, or platform failures
- repeated "agent did not respond / did not finish / forgot identity" incidents
- daily workflow failures where Mission Control says one thing but proof chains say another
- scorecards that compare agent delivery against real receipts, URLs, and closeout evidence

Default failure taxonomy:
- `NetworkPolicyBlocked` - provider/tool blocked by local or external network policy
- `GatewayUnavailable` - gateway process, port, websocket, or reachability failure
- `SessionContextRot` - stale session, stale skill snapshot, identity drift, or outdated config context
- `SkillMissing` - expected skill absent from installed path or session snapshot
- `ToolInvalidArguments` - malformed tool/edit call or bad argument shape
- `ProviderError` - provider/model/API failure not caused by network policy
- `ExternalPlatformBlocked` - X/LinkedIn/Facebook/Feishu/etc. platform/API/login/visibility blocker
- `HumanApprovalRequired` - real approval boundary for external, destructive, production, money, or ambiguous action

Harness workflow:
1. Scan logs and receipts with `scripts/analyze-openclaw-failures.mjs`.
2. Generate same-day agent scorecard with `scripts/daily-agent-scorecard.mjs`.
3. Run `scripts/daily-agent-scorecard.mjs --repair` to create/update recovery tickets for failed, blocked, or pending lanes.
4. Convert repeated classes into an `error`, `experiment`, or promoted rule.
5. Do not call a workflow closed until the scorecard has proof links or explicit blocker evidence.

Repair loop rules:
- Every failed/blocked/pending lane should have a `failureClass`, `repairState`, `nextAction`, `repeatCount7d`, and evidence.
- `ProofMissing`, `UpstreamMissing`, and `HumanApprovalRequired` must not be blindly retried.
- Repeated `agent + lane + failureClass` failures within 7 days should become `EXPERIMENT_REQUIRED`.
- Recovery tickets should be written under `mission-control/data/recovery-tickets-v3/YYYY-MM-DD/`.

## Promotion targets
- `AGENTS.md` → workflow / delegation / execution rules
- `TOOLS.md` → tool gotchas, secrets locations, environment routing rules
- `SOUL.md` → behavior / communication / non-negotiable principles
- Obsidian vault → reusable operator log and content proof asset

## Karen / Mission Control compatibility
This skill is designed to work with stricter ops governance:
- Karen can reference learnings when repeated failures happen
- Mission Control can treat promoted learnings as new operating rules
- recurring blockers can be elevated from chat into tracked operational knowledge
- experiments can test whether a new summary contract, receipt rule, or deploy closeout guardrail actually reduced the failure pattern

## Eval loop rule
When a repeated failure is turning into a new rule/SOP/checklist, do not only log it.
Also:
1. define 3-5 binary evals
2. record the baseline failure state
3. change one thing at a time
4. re-check the same evals
5. classify the change as keep / discard / partial_keep

Use `{baseDir}/references/eval-loop.md` for the experiment format and examples.

## Output goal
A good use of this skill should produce one of:
- a durable learning entry
- a durable error entry
- a durable feature request entry
- a durable experiment entry with binary evals
- a promoted rule in AGENTS.md / TOOLS.md / SOUL.md
- an Obsidian vault operations note

## Important limits
- Logging is not the same as fixing.
- Do not treat a learning entry as closure for a broken deliverable.
- Use this skill to reduce repeated mistakes, not to excuse them.

## References
- `{baseDir}/references/schema.md`
- `{baseDir}/references/promotion-guide.md`
- `{baseDir}/references/eval-loop.md`
- `{baseDir}/references/examples.md`
- `{baseDir}/references/decision-rules.md`

- `{baseDir}/references/eval-loop.md`
- `{baseDir}/references/examples.md`
