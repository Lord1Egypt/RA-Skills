## Description:

Persistent NDJSON event logging with rotation, compression, and retention policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to persist Pilot Protocol event streams as NDJSON logs for audit history, time and topic queries, rotation, compression, retention, and external analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted source names can cause the example logger to write outside the intended /var/log/pilot-events directory.

Mitigation: Validate source names, run the logger as a dedicated low-privilege user, and confirm log paths remain under /var/log/pilot-events before deployment.

Risk: Persistent event logging and automated cleanup can affect operational audit history.

Mitigation: Review retention settings and the 90-day deletion command against operational and compliance requirements before use.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-event-log)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for event subscription logging, jq queries, log rotation, compression, and retention cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
