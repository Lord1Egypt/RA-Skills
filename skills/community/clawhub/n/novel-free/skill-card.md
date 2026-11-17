## Description:

Novel Free is a Chinese long-form fiction workflow that coordinates a main agent and specialized sub-agents for project setup, worldbuilding, character design, outlining, chapter drafting, consistency review, summaries, reader feedback, and maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[228998098](https://clawhub.ai/user/228998098)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and agents use this skill to create and continue Chinese long-form novel projects through structured phases for setup, planning, drafting, review, and revision. It is intended for long-form fiction workflows rather than short stories, poetry, prose essays, translation, or non-fiction writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shell project-management scripts can generate or overwrite files in project directories.

Mitigation: Review scripts before installation or execution and run them only in intended project directories.

Risk: Project names and generated environment files may be unsafe when sourced from untrusted or unusual directories.

Mitigation: Use only project names containing letters, numbers, underscores, or hyphens, and do not source generated environment files from untrusted directories.

Risk: Generated shell values may not be fully validated or escaped.

Mitigation: Validate and shell-escape generated values in project-manager.sh before using the scripts in shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/228998098/skills/novel-free)
- [Skill definition](artifact/SKILL.md)
- [Release metadata](artifact/_meta.json)
- [Phase 0 project initialization workflow](artifact/references/lifecycle-phase0.md)
- [Phase 1 planning workflow](artifact/references/lifecycle-phase1.md)
- [Normal chapter workflow](artifact/references/lifecycle-phase2-normal.md)
- [Resume protocol](artifact/references/resume-protocol.md)
- [Context feeding strategy](artifact/references/context-feeding-strategy.md)
- [Session cache rules](artifact/references/session-cache.md)
- [Summarizer and OOC guardian combo](artifact/references/agent-summarizer-guardian-combo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown project files, Chinese prose, shell command guidance, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local novel project files through phased writing workflows; no network behavior is reported in the skill evidence.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact metadata and SKILL.md describe 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
