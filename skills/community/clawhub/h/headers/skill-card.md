## Description:

Audits HTTP security headers for websites, grades missing protections from A-F, and flags server header information leakage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and site operators use this skill to audit public website HTTP security headers, review missing protections, and identify server information leakage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound web requests to domains supplied by the user.

Mitigation: Use it only for domains you intend to inspect, and avoid private internal services unless testing them from this environment is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/headers)
- [Publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound HTTP requests to user-supplied domains during audits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
