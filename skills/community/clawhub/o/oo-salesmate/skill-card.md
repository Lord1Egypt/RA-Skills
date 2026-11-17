## Description:

This skill uses an OOMOL-connected Salesmate account to inspect records and perform supported CRM actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to retrieve Salesmate information and carry out supported CRM actions through an OOMOL-connected account. It requires confirmation before actions that write or delete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback can run remote installer code whose contents have not been verified.

Mitigation: Review the setup first and use a reviewed, pinned oo CLI release; get approval before installing it or changing other agents' skills.

Risk: The connected account can expose CRM data or carry out writes and deletions.

Mitigation: Limit the Salesmate account's permissions and keep the skill's confirmation requirement for write and delete actions.

## Reference(s):

- [Salesmate API documentation](https://apidocs.salesmate.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Salesmate](https://www.salesmate.io)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that write or delete data require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
