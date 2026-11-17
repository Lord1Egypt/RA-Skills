## Description:

Agent Ping-Pong coordinates a clipboard-based workflow between OpenClaw and a coding agent such as Codex or Claude Code for GitHub PR builds and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to coordinate a human-relayed, two-agent GitHub workflow. OpenClaw writes specs and reviews while Codex or Claude Code implements PRs in a sandbox before approved work is ported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic forwarding of handoff content to a hard-coded Telegram chat can expose task details or route content without adequate per-message review.

Mitigation: Do not enable chat forwarding unless you control the destination and approve each message.

Risk: Clipboard and handoff blocks can expose raw credentials if secrets are included in copied content.

Mitigation: Keep credentials in agent configuration only and remove all API keys, tokens, and secrets from handoff blocks.

Risk: Broad GitHub tokens can let an agent affect repositories outside the intended sandbox or production scope.

Mitigation: Use fine-grained, repo-scoped GitHub tokens with only the permissions needed for contents, pull requests, and metadata.

Risk: Prompt and spec files can influence later agent behavior after installation.

Mitigation: Review prompt/spec files and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/ping-pong)
- [Project homepage](https://github.com/highnoonoffice/agent-ping-pong)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured [AGENT_HANDOFF] blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copy-pasteable handoff blocks, PR review instructions, setup guidance, and merge/porting guardrails.]

## Skill Version(s):

2.8.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
