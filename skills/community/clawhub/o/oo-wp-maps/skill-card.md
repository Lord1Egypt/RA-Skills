## Description:

WP Maps (wpmaps.com). Use this skill for ANY WP Maps request — reading, creating, updating, and deleting data. Whenever a task involves WP Maps, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers with an OOMOL-connected WP Maps account use this skill to read, create, update, and delete product and store records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs a remote CLI installer whose behavior has not been verified.

Mitigation: Review or independently install the CLI, and require approval before running the fallback installer.

Risk: Create, update, and delete actions can change WP Maps account data.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval for deletions.

## Reference(s):

- [WP Maps](https://wpmaps.com/)
- [WP Maps API documentation](https://wpmaps.com/help/wp-maps-api-your-guide-to-integration-and-functionality/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [WP Maps data in JSON with concise action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read, create, update, or delete WP Maps products and stores.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
