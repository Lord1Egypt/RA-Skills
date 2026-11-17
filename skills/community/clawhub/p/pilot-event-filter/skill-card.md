## Description:

Filter and transform events before delivery using pattern matching and jq transforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to filter Pilot Protocol event streams by content, transform payloads with jq, and conditionally republish events to reduce noise or route critical alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forwarded Pilot Protocol events may contain operational or sensitive payload data.

Mitigation: Review event sources, filters, transforms, and publish destinations before running examples.

Risk: The skill guides agents to run pilotctl and jq commands against live event streams.

Mitigation: Install only in environments where Pilot Protocol event streams are expected and command execution is authorized.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-event-filter)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata; SKILL.md metadata lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
