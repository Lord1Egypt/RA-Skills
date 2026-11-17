## Description:

Use SolarWinds Service Desk to read, create, update, and delete incident data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT support staff use this skill to retrieve, create, comment on, update, and delete incidents in SolarWinds Service Desk through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs downloaded code execution without separate approval or integrity checks.

Mitigation: Review and approve CLI installation separately and verify a specific release before installing.

Risk: Automatic skill synchronization may not match the user's expectations.

Mitigation: Decide whether automatic skill synchronization is acceptable before enabling it.

Risk: Ticket data passes through OOMOL, and connector permissions may expose Service Desk data or allow changes.

Mitigation: Connect only the Service Desk permissions needed for the intended tasks.

## Reference(s):

- [SolarWinds Service Desk](https://www.solarwinds.com/service-desk)
- [SolarWinds Service Desk API documentation](https://apidoc.samanage.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-solarwinds-service-desk)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and responses, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the live connector schema; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
