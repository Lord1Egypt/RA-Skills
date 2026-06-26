## Description: <br>
Memory Index guides OpenClaw agents to manage long-term memory through layered indexes, task files, and retrieval rules for lower-token context reconstruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzm232803119-arch](https://clawhub.ai/user/wzm232803119-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to structure persistent memory into active indexes, domain folders, and topic files so agents can resume long-running work, hand off sub-agent tasks, and avoid loading unrelated history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to manage, rewrite, share, and clean up persistent memory without clear approval or rollback controls. <br>
Mitigation: Install only when persistent local memory is desired, require user approval for memory initialization, migration, sub-agent writes, archiving, and cleanup, and review changes before relying on them. <br>
Risk: Persistent memory files may capture secrets or sensitive personal history. <br>
Mitigation: Avoid storing secrets or sensitive personal history in memory files, and set explicit rules for what may be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wzm232803119-arch/memory-index) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create, edit, archive, and clean up local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
