## Description:

Skill completo para lossless-claw (LCM). Incluye instrucciones para instalar el plugin automaticamente.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejay7](https://clawhub.ai/user/yejay7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install or verify the lossless-claw plugin, restart the OpenClaw gateway, and use LCM commands for searching, describing, and expanding conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to install an unpinned third-party OpenClaw plugin and restart the OpenClaw gateway.

Mitigation: Install only after explicit user approval, pin or verify the plugin version, and review the plugin before enabling it.

Risk: The plugin persists and searches broad conversation history in a local database.

Mitigation: Confirm the user is comfortable with local conversation-history storage and apply retention and access controls appropriate to the workspace.

## Reference(s):

- [Lossless Claw Skill on ClawHub](https://clawhub.ai/yejay7/skills/lossless-claw-skill)
- [lossless-claw GitHub repository](https://github.com/Martian-Engineering/lossless-claw)
- [Lossless Context documentation](https://losslesscontext.ai)
- [LCM paper](https://papers.voltropy.com/LCM)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command examples for OpenClaw plugin installation, gateway restart, LCM search, summary inspection, and query expansion.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
