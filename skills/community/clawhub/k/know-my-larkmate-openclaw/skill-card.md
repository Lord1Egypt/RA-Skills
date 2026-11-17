## Description:

Syncs recent Lark context into OpenClaw daily notes for heartbeat runs, recent-work queries, and setup of an OpenClaw-native recent-context workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lobster-de-luo](https://clawhub.ai/user/lobster-de-luo)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to collect recent Lark messages, meetings, documents, wiki content, minutes, and calendar signals into daily memory notes. It helps an agent keep short-term work context current while leaving long-term memory promotion to OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read-only access to private workplace Lark content.

Mitigation: Grant only the read-only scopes and sources needed for the workflow, limit enabled sources where possible, and revoke Lark authorization when the skill is no longer in use.

Risk: Recurring heartbeat jobs can copy selected work context into local OpenClaw memory notes.

Mitigation: Avoid unattended heartbeat use unless needed, review the heartbeat cadence and prompts before enabling them, and keep captured notes factual, recent, and source-linked.

Risk: The workflow depends on lark-cli behavior and authorization remaining trustworthy over time.

Mitigation: Pin the CLI version where practical and run the readiness validation script before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lobster-de-luo/skills/know-my-larkmate-openclaw)
- [Install Checklist](references/install-spec.md)
- [Recent Context Guide](references/recent-context-guide.md)
- [Heartbeat Template](assets/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown daily-note blocks, shell commands, and YAML heartbeat configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends compact, factual, source-linked updates to memory/YYYY-MM-DD.md only when useful new context is found.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
