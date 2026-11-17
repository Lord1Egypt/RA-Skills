## Description:

Openclaw Link helps agent sessions discover peers, delegate tasks, share knowledge, and exchange shared files through a local or network relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple OpenClaw or Claude Code sessions for parallel research, code review, debugging, document drafting, and knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote tasking and shared files can cross weak trust boundaries when the relay is exposed beyond localhost.

Mitigation: Run the relay on localhost where possible; for LAN or tunnel use, require a strong token and add HTTPS/WSS and access controls.

Risk: Incoming tasks, broadcasts, and shared files may contain untrusted instructions or sensitive content.

Mitigation: Review incoming messages before acting on them, avoid uploading sensitive files, and avoid overwriting important local paths with downloaded shared files.

## Reference(s):

- [Protocol Reference](references/protocol.md)
- [ClawHub Skill Page](https://clawhub.ai/sharoonsharif/skills/openclaw-link)
- [Publisher Profile](https://clawhub.ai/user/sharoonsharif)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-line workflows for registering agents, discovering peers, delegating tasks, broadcasting findings, polling messages, and sharing files.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
