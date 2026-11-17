## Description:

Continuous Learning helps an OpenClaw agent identify new tasks, persist conversation memories in MemPalace, run scheduled memory analysis, update core guidance documents, and record lessons for self-correction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[long57777](https://clawhub.ai/user/long57777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to give an agent a persistent learning workflow across projects, including memory synchronization, scheduled analysis, and updates to local guidance files. It is most relevant where users intentionally want conversation history and task lessons to become future agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history and memory excerpts can become persistent future agent context.

Mitigation: Install only in workspaces where persistent memory is intended, and avoid storing secrets or sensitive data in MemPalace or generated learning files.

Risk: Scheduled analysis can send memory excerpts to an external model provider when an analysis API key is configured.

Mitigation: Leave the analysis API key empty until a provider is explicitly approved, and review the configured API endpoint before enabling scheduled analysis.

Risk: The dream analysis workflow can update core guidance files such as AGENTS.md, BOOTSTRAP.md, SOUL.md, MEMORY.md, and TOOLS.md.

Mitigation: Manually review proposed or generated document changes before relying on them in future agent sessions.

Risk: Notification settings can send status messages through an OpenClaw WeChat channel.

Mitigation: Set notification recipients deliberately and disable notifications when messages should remain local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/long57777/skills/long57777-continuous-learning)
- [Publisher profile](https://clawhub.ai/user/long57777)
- [MiniMax OpenAI-compatible API endpoint](https://api.minimax.chat/v1)
- [README.md](artifact/README.md)
- [bootstrap_rules.md](artifact/bootstraps/bootstrap_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON configuration, Python scripts, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local memory, learning, notification queue, and agent guidance files when its setup and scheduled scripts are run.]

## Skill Version(s):

1.1.1 (source: server release metadata; packaged frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
