## Description:

Helps agents connect a Weibo channel to OpenClaw by collecting Weibo AppId and AppSecret credentials and setting them with OpenClaw CLI configuration commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Weibo channel credentials for an OpenClaw installation. It guides the agent to request missing credentials, apply them with OpenClaw CLI commands, and verify the resulting channel configuration when possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Weibo AppSecret through plain CLI commands, which can expose the secret in shared chats, terminal history, transcripts, logs, or command output.

Mitigation: Use it only in a trusted environment, avoid pasting AppSecret values into shared contexts, verify configuration without printing full secret-bearing values, and rotate the AppSecret if exposure occurs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-weibo-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-handling guidance and verification steps for OpenClaw channel configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
