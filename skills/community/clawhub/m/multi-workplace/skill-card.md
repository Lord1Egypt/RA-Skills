## Description:

Multi Workplace helps agents manage multiple project workplaces with per-workspace orchestration, isolated memory, inter-agent communication, IDE context syncing, and deployment notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dickwu](https://clawhub.ai/user/dickwu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to initialize, discover, switch, link, export, import, and monitor project workplaces while coordinating project-specific agents and IDE context files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read project structure and markdown files across workplaces.

Mitigation: Install only for trusted repositories and review workplace scan results before using them to drive agent workflows.

Risk: The skill can write .workplace state, registry data, generated agents, deployment notes, and IDE context files.

Mitigation: Inspect diffs before running init or sync on important projects, and review generated agent files before starting agents.

Risk: Background agent workflows and the chat watcher can act on cloned or user-edited .workplace content.

Mitigation: Avoid running the watcher on untrusted cloned .workplace directories and review chat.md before starting or routing agents.

Risk: The skill can sync workplace summaries to supermemory using per-workplace container tags.

Mitigation: Confirm that project summaries are appropriate for long-term memory before enabling kernel or memory-sync workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dickwu/skills/multi-workplace)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Agent System](references/agent-system.md)
- [Chat Protocol](references/chat-protocol.md)
- [Command Reference](references/commands.md)
- [IDE Sync Guide](references/ide-sync.md)
- [Initialization Guide](references/init-guide.md)
- [Telegram UI](references/telegram-ui.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON or JSONC configuration, shell commands, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .workplace state, IDE context files, agent definitions, deployment notes, registry entries, and exported ZIP or JSON workplace manifests.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
