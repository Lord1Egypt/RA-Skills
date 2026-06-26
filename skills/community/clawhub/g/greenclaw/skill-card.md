## Description: <br>
Token usage analytics and budget alerting for the GreenClaw inference proxy. Query spending, set budget alerts, and track savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanth235](https://clawhub.ai/user/srikanth235) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of the GreenClaw inference proxy use this skill to query token usage, cost, savings, request traces, and budget alerts from telemetry data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run an unpinned external GreenClaw CLI that was not included in the reviewed artifact. <br>
Mitigation: Install the CLI only from a trusted source, preferably with a pinned version, and review the package before execution. <br>
Risk: Usage reports and telemetry database paths may expose sensitive cost, model, provider, request, or savings information. <br>
Mitigation: Treat generated reports and the GREENCLAW_TELEMETRY_DB data source as sensitive and redact details before sharing. <br>
Risk: Budget alert commands can create, change, or remove alert rules that affect operational cost monitoring. <br>
Mitigation: Require explicit user approval before creating, modifying, checking, or removing budget alerts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON-derived tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands output JSON; cost values should be rounded to 2 decimal places.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
