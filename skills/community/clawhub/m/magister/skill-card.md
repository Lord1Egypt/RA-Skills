## Description:

Fetch schedule, grades, and infractions from the Magister school portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghuron](https://clawhub.ai/user/ghuron)

### License/Terms of Use:

MIT-0

## Use Case:

External users with authorized Magister accounts use this skill to retrieve student lists, schedules, grades, and absence or infraction records from the Magister portal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles school account credentials and sensitive student data.

Mitigation: Only run it with credentials you are authorized to use, and review the skill before installation.

Risk: The security evidence reports a token-handling weakness involving the apiGet host override.

Mitigation: Remove or validate the host override so tokens cannot be sent to non-Magister domains.

## Reference(s):

- [Magister portal](https://magister.net)
- [ClawHub skill page](https://clawhub.ai/ghuron/skills/magister)
- [ClawHub publisher profile](https://clawhub.ai/user/ghuron)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-producing CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node plus MAGISTER_HOST, MAGISTER_USER, and MAGISTER_PASSWORD environment variables.]

## Skill Version(s):

1.1.1 (source: release metadata, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
