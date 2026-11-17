## Description:

Use this skill to read, create, and update TheHive alerts and cases through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and incident responders use this skill to retrieve TheHive alerts and cases and create alerts or cases in a connected TheHive 4 instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may execute installer code that has not been independently verified.

Mitigation: Review and install the oo CLI separately before use; the external installer and service implementations have not been verified.

Risk: Automatic skill synchronization can make persistent changes across agent environments.

Mitigation: Disable automatic skill synchronization if you do not want changes to propagate across your agents.

Risk: The connected account may expose incident data or permissions beyond what a task needs.

Mitigation: Connect only the TheHive permissions needed and consider whether incident data may pass through OOMOL.

## Reference(s):

- [TheHive](https://thehive-project.org)
- [TheHive API documentation](https://docs.strangebee.com/thehive/api-docs/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [TheHive skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-thehive)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [oo CLI commands with JSON payloads and TheHive action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return TheHive data; create actions write alerts or cases and require user confirmation.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter; evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
