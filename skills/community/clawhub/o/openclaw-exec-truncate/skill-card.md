## Description:

AI agent tool for compressing/executing shell commands with domain-aware output truncation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ether-btc](https://clawhub.ai/user/ether-btc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to shorten verbose shell command output from git, search, directory listing, and build commands while preserving the most relevant lines for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Truncation can hide command output that later proves important for debugging, review, or agent decisions.

Mitigation: Use it only where losing nonessential command output is acceptable, and keep an easy way to rerun commands without truncation.

Risk: Plugin-style output interception can materially affect what users and agents see from shell commands.

Mitigation: Review the skill carefully before installation and verify the exact package and version before activating it in the OpenClaw gateway.

Risk: Oversized-output logging can be inappropriate for commands that may include secrets or sensitive paths.

Mitigation: Avoid enabling oversized-output logging for secret-bearing workflows, or keep that logging disabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ether-btc/skills/openclaw-exec-truncate)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/plugins/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and TypeScript-oriented guidance with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shortened command-output text and configuration guidance; truncation can omit raw command details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
