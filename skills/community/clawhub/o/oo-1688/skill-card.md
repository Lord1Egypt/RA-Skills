## Description:

1688 (1688.com). Use this skill for ANY 1688 request — reading, creating, updating, and deleting data. Whenever a task involves 1688, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read 1688 account data and manage products, orders, logistics, refunds, and related records through their connected account. State-changing actions require the user to confirm the exact action and payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute remote installer code, and installer contents were not verified.

Mitigation: Review the oo CLI and its installer before installing; follow the publisher's setup guidance.

Risk: Setup may introduce additional agent skills through startup synchronization.

Mitigation: Review the skills installed by setup and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when appropriate.

Risk: Connected account actions can change or remove 1688 data.

Mitigation: Limit connected-account permissions and retain the skill's confirmation requirements for write and destructive actions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [1688 API documentation](https://open.1688.com/doc/apiAuth.htm)
- [1688 homepage](https://www.1688.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON request payloads; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions marked write or destructive require user confirmation; destructive actions also require explicit approval.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
