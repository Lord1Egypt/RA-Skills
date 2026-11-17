## Description:

Token usage analytics and budget alerting for the GreenClaw inference proxy. Query spending, set budget alerts, and track savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanth235](https://clawhub.ai/user/srikanth235)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query GreenClaw token usage, cost, savings, trends, raw trace statistics, and budget alert status. It can also guide agents through creating, checking, and removing GreenClaw budget alert rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run an unpinned external GreenClaw CLI through npx, so command behavior can change at runtime.

Mitigation: Use a pinned, trusted GreenClaw CLI version or a locally installed build from a locked dependency set before allowing the agent to run commands.

Risk: The skill includes commands that create and remove budget alert rules.

Mitigation: Require explicit confirmation before the agent creates, changes, checks, or removes alert rules, and review the resulting JSON output.

Risk: The telemetry database path can expose unintended local data if pointed outside the intended GreenClaw telemetry store.

Mitigation: Restrict GREENCLAW_TELEMETRY_DB to the intended GreenClaw SQLite database path and avoid exposing unrelated credentials or files in the command environment.

## Reference(s):

- [GreenClaw ClawHub skill page](https://clawhub.ai/srikanth235/skills/greenclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON-derived tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands invoke the GreenClaw CLI and expect JSON responses; GREENCLAW_TELEMETRY_DB may set the SQLite telemetry database path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
