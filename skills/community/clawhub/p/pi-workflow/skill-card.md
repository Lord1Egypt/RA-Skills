## Description:

Workflow orchestration for Pi's task management, self-improvement, and code quality standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-tw](https://clawhub.ai/user/kai-tw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to plan multi-step work, track progress, capture lessons from mistakes, and apply verification gates before completing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages agents to persist lessons, errors, feature requests, and memory-like notes that may include private or sensitive content.

Mitigation: Decide allowed write locations before use, avoid logging secrets or private user content, and review lesson files before retaining or sharing them.

Risk: The workflow describes promoting learned rules into future-governing files such as AGENTS.md, SOUL.md, TOOLS.md, and MEMORY.md.

Mitigation: Require explicit human approval before promoting any lesson into governance, memory, or published skill files.

Risk: The bundled sync script can overwrite the skill's references/lessons.md with content derived from workspace lessons.

Mitigation: Run the sync script in dry-run mode first and review diffs before committing, publishing, or pushing synchronized lesson content.

## Reference(s):

- [Workflow Orchestration](references/workflow_orchestration.md)
- [Lessons](references/lessons.md)
- [Phase 1 and Phase 2 Enhanced Lessons](references/phase1-phase2-enhanced-lessons.md)
- [Lessons Update Guide](references/lessons_update_guide.md)
- [Pi Workflow ClawHub Skill Page](https://clawhub.ai/kai-tw/skills/pi-workflow)
- [Srishti Codes workflow inspiration](https://x.com/srishticodes/status/2025254119636959701)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update workspace task, lesson, error, feature request, memory, and governance files.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
