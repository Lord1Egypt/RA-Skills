## Description:

Operate Slack through an OOMOL-connected account to read, search, and manage Slack conversations, messages, reactions, and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use the skill to find Slack information and carry out approved actions such as posting messages, managing reactions, and handling files through their connected Slack account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute remote code that was not inspected and may synchronize skills to other agent hosts.

Mitigation: Review and verify CLI installation separately, and explicitly control any changes to other agent hosts.

Risk: The connector processes data from the connected Slack account, and write or destructive actions can change Slack content.

Mitigation: Grant only the needed access and retain approval safeguards for posting and deletion actions.

## Reference(s):

- [Slack](https://slack.com)
- [Slack Web API documentation](https://docs.slack.dev/apis/web-api/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses, shell commands, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected Slack account; posting and deletion actions require user confirmation.]

## Skill Version(s):

1.0.13 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
