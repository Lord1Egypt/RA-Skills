## Description:

Open Memory System provides a three-layer persistent memory framework for AI agents, covering working memory, short-term session memory, and long-term preferences, entities, events, persona, and episodic records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jochenyang](https://clawhub.ai/user/jochenyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory to an OpenClaw agent, including preference capture, entity and event records, short-term summaries, and scheduled memory maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic hooks and scheduled tasks can persist and process agent memory without direct user action.

Mitigation: Enable only the hooks and cron jobs that are required, review their schedules and triggers, and disable them in shared or sensitive workspaces until approved.

Risk: Persistent memory files may contain sensitive preferences, events, entities, or session summaries.

Mitigation: Store MEMORY_DIR in a private least-privilege location, inspect retained memory regularly, and apply cleanup policies before using the skill with confidential data.

Risk: The security scan reports unsafe file-writing and code-execution paths, including filename validation and cleanup index.py execution concerns.

Mitigation: Fix and review those paths before relying on the skill in a shared, production, or sensitive workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jochenyang/skills/open-memory-system)
- [Publisher Profile](https://clawhub.ai/user/jochenyang)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Cron Configuration Guide](artifact/crons/memory-crons.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create and update local memory files through Python CLI commands, OpenClaw hooks, and scheduled cron tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
