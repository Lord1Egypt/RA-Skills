## Description:

Analyze OpenClaw session JSONL history for cost spikes, tool-call anomalies, and behavior regressions with jq + rg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect session JSONL logs during incident forensics, including cost spikes, tool-call drift, behavior regressions, and prior-chat context lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search broad cross-session conversation history, which may expose unrelated transcript content or secrets from prior conversations.

Mitigation: Require an explicit scope such as a session ID, date range, or incident window, and avoid returning unrelated transcript content or secrets.

Risk: Historical agent session logs may contain sensitive operational details.

Mitigation: Install and use only where operators are authorized to inspect the selected agent's historical session logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielsinewe/skills/openclaw-session-log-forensics)
- [Publisher Profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and jq/rg examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and rg; outputs should be scoped to the requested session, date range, or incident window.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
