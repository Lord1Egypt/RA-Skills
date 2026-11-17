## Description:

Manage multiple OpenAI OAuth accounts in OpenClaw by saving account snapshots, switching active accounts, checking cached 5-hour and weekly usage, rotating near quota exhaustion, and falling back to a backup model when OpenAI accounts are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tutouguai1933](https://clawhub.ai/user/tutouguai1933)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage multiple OpenAI Codex OAuth accounts, inspect active account and quota state, and automate account rotation or fallback model selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and rewrite OpenClaw OAuth credentials across configured agents.

Mitigation: Install only in environments where account switching is expected, treat the snapshot directory as sensitive credential storage, and review status output before switching accounts.

Risk: The usage endpoint is configurable and could be pointed at an untrusted host.

Mitigation: Pin unattended use to a trusted HTTPS OpenAI or ChatGPT usage host before enabling scheduled checks.

Risk: Account names influence stored snapshot paths and metadata.

Mitigation: Use validated, simple account names and reject path traversal characters before adding accounts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tutouguai1933/skills/openclaw-openai-multi-account)
- [ChatGPT usage endpoint used by the artifact](https://chatgpt.com/backend-api/wham/usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local commands that read and rewrite OpenClaw OAuth account snapshots and agent auth configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
