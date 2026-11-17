## Description:

Personal AI Memory System is a personal journaling and memory skill that helps an AI assistant maintain local Markdown records, summarize life patterns, support goal tracking, and provide decision-analysis guidance from user-provided history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn an AI assistant into a local personal memory system for daily journaling, quick notes, personal retrospectives, goal tracking, and decision scenario analysis. It is intended for user-triggered use with sensitive personal records stored under a local memory directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist highly sensitive personal history and reuse it in later interactions.

Mitigation: Keep the memory directory private, use encrypted local storage where possible, restrict filesystem permissions, and avoid committing memory files to source control.

Risk: Broad activation language can cause the assistant to load or update personal memory in more situations than intended.

Mitigation: Keep invocation explicit, avoid broad or global auto-trigger rules, and confirm the requested memory task before reading or writing personal records.

Risk: The documented installer command is unpinned.

Mitigation: Use a pinned or reviewed installer source and inspect the skill package before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenchen913/skills/personal-memory-system)
- [Project Homepage](https://github.com/ChenChen913/memory-system)
- [README_EN.md](README_EN.md)
- [Initialization Flow](references/00-initialization.md)
- [Present Dimension: Daily Recording System](references/01-present.md)
- [Past Dimension: Life Archive System](references/02-past.md)
- [Future Dimension: Decision Analysis, Goal Tracking, and State Prediction](references/03-future.md)
- [Special Protocols](references/05-protocols.md)
- [AI Voice and Persona Specification](references/06-ai-voice.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, local Markdown memory files, and optional shell commands for setup or privacy configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persistent local personal records, summaries, reports, goal updates, decision analyses, and privacy setup commands.]

## Skill Version(s):

3.1.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
