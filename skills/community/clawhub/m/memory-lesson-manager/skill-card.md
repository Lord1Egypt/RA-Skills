## Description: <br>
Memory Lesson Manager helps agents maintain structured workspace memory by recording lessons, organizing HOT/WARM/COLD lesson tiers, recovering state, searching lessons, promoting frequently used lessons, archiving older lessons, and extracting reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tank2737](https://clawhub.ai/user/tank2737) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, validate, search, promote, archive, and migrate workspace lesson records. It is intended for teams that want persistent local memory for errors, corrections, best practices, decisions, projects, people notes, and reusable skill extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's scripts can create, edit, move, and archive files under local memory, state, and skills directories. <br>
Mitigation: Run dry-run modes first, inspect planned changes, and keep backups before initialization, migration, promotion, archive, or restore operations. <br>
Risk: Migration and rollback workflows include file moves and removal commands that can affect existing lesson structures. <br>
Mitigation: Follow the documented conservative migration path, verify backups before proceeding, and review rollback commands before running them. <br>
Risk: Promoted lessons or extracted skills can preserve incorrect or outdated project guidance. <br>
Mitigation: Review lesson content before promotion or extraction, validate diaries and lesson links, and prune obsolete HOT or COLD entries during maintenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tank2737/memory-lesson-manager) <br>
- [Usage guide](references/usage-guide.md) <br>
- [Usage examples](references/usage-examples.md) <br>
- [Migration guide](references/migration-guide.md) <br>
- [Optimization proposals](references/optimization-proposals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory, state, and skill files when the included scripts are run outside dry-run mode.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
