## Description:

Use this skill to read, create, and update Google Chat data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Google Chat account can retrieve spaces, messages, and members, or send plain-text messages to a space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded software and make persistent changes to other agents.

Mitigation: Review CLI installation separately, use a verified fixed release, and check or disable unwanted bundled-skill synchronization before running it.

Risk: A message could reach the wrong recipient or contain unintended text if its details are not checked.

Mitigation: Connect only the intended Google Chat account and review the recipient and message text before sending.

## Reference(s):

- [Google Chat API reference](https://developers.google.com/workspace/chat/api/reference/rest)
- [Google Chat](https://workspace.google.com/products/chat/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON connector results, plain-text messages, and shell commands for connector actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message sending changes Google Chat state and requires confirmation; cards and attachments are not supported.]

## Skill Version(s):

1.0.5 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
