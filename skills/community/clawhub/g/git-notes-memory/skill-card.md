## Description: <br>
Provides a git-notes-backed, branch-aware memory system that lets Claude Code store, retrieve, update, and organize project context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mourad-ghafiri](https://clawhub.ai/user/mourad-ghafiri) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to preserve project decisions, preferences, tasks, learnings, and branch-specific context across coding sessions. It is intended for repositories where local git-notes storage and automatic memory maintenance are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores project and user context while instructing the agent to operate silently. <br>
Mitigation: Install only when automatic persistent memory is intended; add local rules requiring approval before storing sensitive context and periodically inspect or delete stored notes. <br>
Risk: The memory tool can mutate git state by using git notes and, when needed, initializing git configuration or creating an empty initial commit. <br>
Mitigation: Use it only in repositories where git notes, local git config changes, and an empty initial commit are acceptable; test in a disposable repository before enabling it on important projects. <br>
Risk: Stored memories may contain secrets, personal data, or stale project assumptions if the agent records them automatically. <br>
Mitigation: Exclude secrets and personal data from memory operations, review stored notes regularly, and delete or update stale entries with the provided forget and update commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mourad-ghafiri/git-notes-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill integration guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and compact JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local git notes for persistent branch-aware memory; no external dependencies are documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
