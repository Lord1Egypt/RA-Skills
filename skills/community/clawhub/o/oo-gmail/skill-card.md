## Description:

Use the OOMOL-connected Gmail account to read and manage messages, drafts, labels, filters, mailbox settings, and threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Gmail account can ask an agent to search and read mail, manage drafts and organization, inspect settings, and send or reply to messages. The skill can also change mailbox state, so writes and destructive actions require user confirmation as described in the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded CLI code immediately.

Mitigation: Review and approve the CLI installation separately, preferably using a verified release.

Risk: Downloading an attachment uploads it to Connector transit storage without a confirmation step in the documented action flow.

Mitigation: Require confirmation before upload and check the transit storage access and retention rules.

Risk: The CLI may synchronize skills automatically.

Mitigation: Review the automatic skill synchronization behavior before first use.

## Reference(s):

- [Gmail API documentation](https://developers.google.com/workspace/gmail/api/guides)
- [Gmail](https://workspace.google.com/gmail/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub Gmail skill release](https://clawhub.ai/oomol/skills/oo-gmail)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Gmail connector action results and status messages, typically as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected Gmail action; actions may read mailbox data or make requested changes.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
