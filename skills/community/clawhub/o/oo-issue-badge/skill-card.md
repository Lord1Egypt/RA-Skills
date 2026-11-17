## Description:

Use the oo CLI to read IssueBadge records, list badge templates, and issue badges through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and badge administrators use this skill to retrieve badge records and templates, and to issue badges through their connected IssueBadge account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to install a CLI version that the security review could not verify.

Mitigation: Review and install a verified oo CLI version separately before use.

Risk: Startup synchronization may make changes to other agent skills.

Mitigation: Review the publisher's synchronization behavior and set OO_SKILLS_SYNC_DISABLED=1 if automatic skill changes are unwanted.

Risk: Using the integration shares credentials and requested recipient data with OOMOL; issuing a badge can send a notification email.

Mitigation: Confirm the connection, public badge details, recipient data, and notification email before issuance.

## Reference(s):

- [IssueBadge](https://issuebadge.com)
- [IssueBadge REST API documentation](https://issuebadge.com/features/integrations/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples; actions return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas define request fields; responses include data and execution metadata.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
