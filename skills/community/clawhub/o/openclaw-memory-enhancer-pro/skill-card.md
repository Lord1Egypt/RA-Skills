## Description:

Memory Enhancer Pro helps OpenClaw users search, summarize, classify, and optimize local AI memory files with token analysis and scheduled maintenance utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect local memory files, find prior context, summarize current session state, classify memory content, and review token-optimization suggestions. It is most appropriate when the user accepts local file reads and writes and explicitly reviews cleanup or scheduled task behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw memory plus USER.md, SOUL.md, and AGENTS.md metadata.

Mitigation: Review the scripts before installation and avoid storing sensitive information in files the skill inspects.

Risk: The skill can write token statistics, logs, and scheduled-task configuration.

Mitigation: Run analysis manually first, inspect generated files, and enable scheduled tasks only after confirming the behavior.

Risk: The cleanup behavior can delete old date-named memory files when explicitly executed.

Mitigation: Keep backups of ~/.openclaw/, use dry-run style review where available, and avoid negative or untrusted --days values.

Risk: The advertised Pro semantic search and compression claims may overstate the implementation.

Mitigation: Treat search, classification, and token savings as heuristic output and validate important results before relying on them.

## Reference(s):

- [Memory Enhancer Pro on ClawHub](https://clawhub.ai/williamwg2025/skills/openclaw-memory-enhancer-pro)
- [README_EN.md](README_EN.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text and Markdown guidance with JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file analysis may produce token statistics, optimization suggestions, schedule settings, and cleanup status.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata; packaged SKILL.md frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
