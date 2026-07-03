## Description: <br>
End-of-session knowledge cleanup reconciles project documentation and agent memory against the codebase so knowledge stays current, concise, and useful. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill at the end of a coding session or milestone to update README, docs, CLAUDE.md/AGENTS.md, and agent memory from the current code state. It is intended for documentation and knowledge-base reconciliation, not general code cleanup or unrelated tidying tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause broad documentation, instruction-file, or memory changes, including deletion or persistent state updates. <br>
Mitigation: Use it on a clean branch, review the proposed file list before changes, and require confirmation before deletion or global memory/config updates. <br>
Risk: Incorrect reconciliation can leave project guidance misleading or out of date. <br>
Mitigation: Compare proposed changes against the codebase, run the included audit where applicable, and review generated documentation before relying on it. <br>
Risk: Broad rollback commands can discard unrelated work while recovering from a bad cleanup run. <br>
Mitigation: Back up or stash work before cleanup and avoid broad rollback commands unless the intended changes are isolated and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/neat) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.en.md](artifact/README.en.md) <br>
- [agent-paths.md](artifact/references/agent-paths.md) <br>
- [sync-matrix.md](artifact/references/sync-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with proposed file edits and shell commands when verification is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify project documentation, agent instruction files, and memory files when the user approves the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
