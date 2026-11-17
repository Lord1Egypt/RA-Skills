## Description:

像发消息一样记录灵感、想法、知识、收支、日记、任务和引用，并让 the agent classify, tag, title, store, search, summarize, and export those notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yankj](https://clawhub.ai/user/yankj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture short messages as structured personal notes, expenses, diary entries, tasks, quotes, and knowledge snippets. The agent classifies each entry, generates tags and titles, writes Markdown records, and supports search, summaries, statistics, and export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive chat, diary, task, and financial content in local note files.

Mitigation: Avoid recording secrets, review saved files under memory/just-note, and configure storage and backup practices before routine use.

Risk: Automatic or low-friction capture can save content the user did not intend to retain.

Mitigation: Use an explicit invocation habit and review newly created notes before treating them as a durable personal record.

Risk: Installation and publishing examples use @latest ClawHub CLI commands.

Mitigation: Pin or verify CLI versions and commands before copying them into an installation or release workflow.

Risk: The release is described by security evidence as unfinished and under-scoped for privacy and installation safety.

Mitigation: Test installation and note-writing behavior in a non-sensitive workspace before deploying it for regular use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yankj/skills/just-note-ai)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [AI Message Handler Guide](artifact/AI-HANDLER.md)
- [Test Report](artifact/TEST-REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes with YAML frontmatter, JSON classification objects, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes records under memory/just-note and may include generated titles, tags, observations, amount, currency, and source metadata.]

## Skill Version(s):

0.2.0 (source: server release metadata and CHANGELOG.md, released 2026-03-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
