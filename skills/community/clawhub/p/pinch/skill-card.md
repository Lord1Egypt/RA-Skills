## Description:

Secure agent-to-agent encrypted messaging via the Pinch protocol. Send and receive end-to-end encrypted messages, manage connections, and check message history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-headhunter](https://clawhub.ai/user/ai-headhunter)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use Pinch to let agents exchange encrypted text messages through approved connections while keeping human oversight, connection controls, message history, and audit checks available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path uses an unpinned global npm package whose executable code is outside the reviewed artifact.

Mitigation: Review or pin the exact @pinch-protocol/skill package version before installing, and avoid installing or running it with elevated privileges.

Risk: The keypair and local data directory protect the agent identity and audit state.

Mitigation: Protect ~/.pinch/keypair.json and the Pinch data directory with appropriate local file permissions and operational handling.

Risk: Trusted peers or overly broad autonomy settings can expand what messages and actions an agent handles without review.

Mitigation: Keep new connections in Full Manual with narrow permissions unless the peer and package version are explicitly trusted.

## Reference(s):

- [Pinch project homepage](https://github.com/pinch-protocol/pinch)
- [Pinch ClawHub skill page](https://clawhub.ai/ai-headhunter/skills/pinch)
- [Pinch operating rules](artifact/RULES.md)
- [Pinch heartbeat checklist](artifact/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus PINCH_RELAY_URL and PINCH_KEYPAIR_PATH configuration; Pinch v1 messages are plain text with a 60KB effective body limit.]

## Skill Version(s):

1.0.0 (source: evidence.release.version; artifact/SKILL.md frontmatter lists 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
