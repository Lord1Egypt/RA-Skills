## Description:

Implements cryptographic governance for AI agents by verifying actions against policies and recording signed, tamper-evident audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knuckles-stack](https://clawhub.ai/user/knuckles-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams building AI agents use this skill to add Kevros governance checks before high-impact actions and to create signed audit records for compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration sends selected agent action metadata to the Kevros/TaskHawk governance service.

Mitigation: Redact or schema-limit action_payload values and avoid sending secrets or personal data.

Risk: API keys and SDK dependencies are required for some integration paths.

Mitigation: Keep API keys out of source code and logs, and pin or verify SDK package versions before production use.

Risk: Governance records and service logs may have retention implications.

Mitigation: Review the provider's retention and logging terms before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knuckles-stack/skills/kevros-governance)
- [TaskHawk Tech website](https://www.taskhawktech.com)
- [Kevros API docs](https://governance.taskhawktech.com/api)
- [Kevros quickstart](https://www.taskhawktech.com/quickstart)
- [Kevros playground](https://www.taskhawktech.com/playground)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, SDK installation commands, and governance integration patterns.]

## Skill Version(s):

0.3.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
