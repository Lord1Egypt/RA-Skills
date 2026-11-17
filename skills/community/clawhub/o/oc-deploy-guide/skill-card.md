## Description:

Interactive deployment guide for OpenClaw local capabilities, including the Memory Stack, vid2md, WeChat plugin, and maintenance cron jobs with confirmation gates between phases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ottoprua](https://clawhub.ai/user/ottoprua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up or extend a local OpenClaw instance with memory search, context compression, video-to-Markdown conversion, WeChat integration, and scheduled maintenance. The skill guides the agent through prerequisite checks, installation commands, configuration snippets, verification steps, and user confirmations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install mutable third-party software and dependencies.

Mitigation: Review each command before execution, prefer pinned versions or verified releases, and use isolated environments for npm, Bun, and Python packages.

Risk: The deployment flow can create persistent automation through cron jobs.

Mitigation: Enable cron jobs only after reviewing their messages, schedule, timezone, and filesystem access.

Risk: The WeChat integration may read or modify chat-related data depending on local configuration.

Mitigation: Enable WeChat integration only after reviewing allowed groups, bot trigger behavior, accessibility permissions, and data access.

Risk: Installer and path commands can affect local OpenClaw configuration and workspace files.

Mitigation: Confirm canonical target paths and inspect configuration changes before restarting OpenClaw services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ottoprua/skills/oc-deploy-guide)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw memory manager](https://github.com/OttoPrua/openclaw-memory-manager)
- [vid2md](https://github.com/OttoPrua/vid2md)
- [OpenClaw WeChat plugin](https://github.com/OttoPrua/openclaw-wechat-bot)
- [Memory Manager Skill on ClawHub](https://clawhub.ai/OttoPrua/agent-memory-protocol)
- [Cron reference configs](https://github.com/OttoPrua/openclaw-memory-manager/tree/main/cron)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive phase-by-phase guidance with prerequisite checks, verification steps, and confirmation gates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
