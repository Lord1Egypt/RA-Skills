## Description:

OpenClaw Docs helps agents cache, search, fetch, and track OpenClaw documentation so answers can cite current docs links and page text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jszesze](https://clawhub.ai/user/jszesze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer OpenClaw setup, configuration, CLI, channel, automation, architecture, and troubleshooting questions with grounded documentation lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell commands can accept broad URL or path-like inputs and may fetch from non-doc services, write outside the intended cache, or print local file contents.

Mitigation: Run the skill only in controlled environments, avoid untrusted command inputs, avoid full URLs or local file paths, and prefer a version constrained to docs.openclaw.ai with cache path validation.

## Reference(s):

- [OpenClaw docs index](https://docs.openclaw.ai/llms.txt)
- [OpenClaw Telegram docs](https://docs.openclaw.ai/channels/telegram)
- [OpenClaw Docs ClawHub release](https://clawhub.ai/jszesze/skills/jszesze-openclaw-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and documentation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cached documentation paths, search results, fetched Markdown excerpts, and snapshot comparisons.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
