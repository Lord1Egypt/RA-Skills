## Description:

Provides usage guidance and runtime troubleshooting for MaxClaw and OpenClaw, using trusted documentation sources and escalation guidance when issues cannot be confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisliu16](https://clawhub.ai/user/krisliu16)

### License/Terms of Use:


## Use Case:

Developers, operators, and support agents use this skill to answer MaxClaw/OpenClaw setup questions, diagnose runtime failures, and decide when to stop and escalate to official support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper may activate on generic troubleshooting or how-to requests outside the intended MaxClaw/OpenClaw support context.

Mitigation: Use it primarily for MaxClaw/OpenClaw support and verify that the cited documentation applies to the user's deployment.

Risk: Troubleshooting may involve configuration files, irreversible actions, or external messages.

Mitigation: Require explicit user approval before modifying configuration, performing irreversible operations, or sending data externally.

Risk: A runtime problem may not have a clear match in trusted documentation.

Mitigation: Stop independent attempts, report sources consulted and findings, and redirect the user to official OpenClaw community support.

## Reference(s):

- [OpenClaw Official Docs](https://docs.openclaw.ai/)
- [OpenClaw CLI Reference](https://docs.openclaw.ai/cli)
- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/gateway)
- [OpenClaw Channel Configuration](https://docs.openclaw.ai/channels)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [OpenClaw Cron Documentation](https://docs.openclaw.ai/cron)
- [MiniMax Official Feishu Documentation](https://vrfi1sk8a0.feishu.cn/wiki/YwEZwj3iuixCK9koFeacwvC6n9d)
- [OpenClaw Community](https://discord.com/invite/clawd)
- [Trusted Sources - MaxClaw Helper](artifact/references/trusted-sources.md)
- [Community Support Template](artifact/references/community-template.md)
- [ClawHub Skill Page](https://clawhub.ai/krisliu16/skills/maxclaw-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with citations, checklists, and inline shell commands when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies in the user's language and escalates when trusted documentation does not support a safe answer.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
