## Description:

Persistent structured memory system for OpenClaw agents with SQLite storage, hybrid search, rule-based capture, LLM-powered daily reflection, and adaptive weekly trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oleglegegg](https://clawhub.ai/user/oleglegegg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Oracle to give OpenClaw agents persistent cross-session memory, retrieval, and memory hygiene for long-running workflows. It is suited for private or carefully scoped agent contexts where users want structured recall, guardrails, and continuity after compaction or restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store and reuse conversation content across sessions with weak scoping.

Mitigation: Review before installation, use private contexts, avoid shared or group contexts until isolation is enforced, and inspect stored memory before enabling automated workflows.

Risk: The HEAVY process can send daily logs and memory state to an external or configurable endpoint.

Mitigation: Use LIGHT-only mode by leaving ANTHROPIC_API_KEY unset unless external processing is acceptable, and do not point api.base_url at another endpoint while using ANTHROPIC_API_KEY.

Risk: Ordinary text can be promoted into always-active rules or guardrails.

Mitigation: Review captured guardrails and reflection output, keep the confidence gate enabled, and manually remove or archive incorrect persistent rules.

Risk: Uninstall and maintenance paths can delete memory data or reflection files.

Mitigation: Avoid --force uninstall, export or back up memory data first, and inspect stats before enabling cron or deletion paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oleglegegg/skills/memory-oracle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall output is budgeted by configuration; default recall budget is about 2000 tokens.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
