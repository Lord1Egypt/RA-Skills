## Description:

GetResponse (getresponse.com). Use this skill for ANY GetResponse request — reading, creating, updating, and deleting data. Whenever a task involves GetResponse, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read and manage GetResponse campaigns, contacts, newsletters, tags, custom fields, and newsletter statistics through a connected account. Write actions require confirmation, and destructive actions require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded installers, and the CLI may synchronize skill changes across agents.

Mitigation: Review setup before use; explicitly approve and verify the CLI installation and cross-agent synchronization.

Risk: Actions can create, update, or permanently delete GetResponse records.

Mitigation: Confirm write payloads and effects, explicitly approve destructive targets, and preserve the skill's required approval steps.

## Reference(s):

- [ClawHub GetResponse skill page](https://clawhub.ai/oomol/skills/oo-getresponse)
- [GetResponse API documentation](https://apidocs.getresponse.com/v3)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [GetResponse website](https://www.getresponse.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Connector action results and JSON request payloads, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected GetResponse account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
