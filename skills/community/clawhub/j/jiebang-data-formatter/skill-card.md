## Description:

Formats and converts developer data, including JSON/YAML, XML, SQL, numeric bases, HTML entities, and cron expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert, validate, format, or describe common data formats during software development and operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied data may be sent to an external service without disclosed retention or access controls.

Mitigation: Do not use the skill on secrets, credentials, proprietary configurations, private SQL, personal data, or regulated content unless the service has been reviewed and trusted.

Risk: Requests use an admin credential for service access.

Mitigation: Replace the admin key with a narrowly scoped service credential and disclose the remote processing requirement before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebang-tools/skills/jiebang-data-formatter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON results containing converted, formatted, validated, or described data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include formatted JSON, YAML, XML, SQL, base-conversion values, HTML entities, cron descriptions, validation status, and next-run timestamps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
