## Description:

Install, configure, and troubleshoot the HiLight OpenClaw plugin as a user-facing setup workflow for connecting OpenClaw to HiLight, installing @art_style666/hi-light, updating channel configuration, rotating the HiLight API key or websocket URL, and diagnosing connection issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongcong](https://clawhub.ai/user/gongcong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and configure the HiLight OpenClaw plugin, safely collect a HiLight API key, write the hi-light channel configuration through OpenClaw commands, restart the gateway, and troubleshoot connection failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow handles a HiLight API key that could be exposed in terminal history, dry-run output, logs, or agent transcripts.

Mitigation: Treat the key as secret input, avoid echoing real keys in responses or dry-run transcripts, and rotate any key that was exposed.

Risk: The skill installs and enables the third-party @art_style666/hi-light plugin and configures an OpenClaw channel.

Mitigation: Review the skill and plugin source before installing, and use the skill only if the publisher and plugin source are trusted.

Risk: Default channel settings use an open dmPolicy and wildcard allowFrom list.

Mitigation: Set a restrictive dmPolicy and explicit allowFrom list during configuration instead of accepting the wildcard defaults.

## Reference(s):

- [HiLight OpenClaw user flow](references/user-flow.md)
- [ClawHub skill page](https://clawhub.ai/gongcong/skills/hi-light-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a HiLight API key and optional websocket URL, then guide OpenClaw plugin installation, channel configuration, validation, and gateway restart.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
