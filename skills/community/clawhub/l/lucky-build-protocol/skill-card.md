## Description: <br>
Guides agents through a repeatable build-queue workflow for selecting tasks from NEXT_TASKS.md, executing them, verifying work, checkpointing, and handing off across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to continue ordered project work from NEXT_TASKS.md with baseline testing, checkpoints, verification, and structured handoff notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run shell commands, create commits, call local enforcement scripts, and submit curl requests. <br>
Mitigation: Require explicit user confirmation before command execution, commits, backups, curl submissions, and local enforcement scripts. <br>
Risk: The workflow references a hardcoded SSH key path and remote host for Jinx status checks. <br>
Mitigation: Remove or gate SSH and Jinx steps unless the operator has verified the host, key, and intended environment. <br>
Risk: Delegated agents and memory logs may expose project context or sensitive information. <br>
Mitigation: Review delegated tasks before submission and avoid placing secrets or sensitive data in memory logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/lucky-build-protocol) <br>
- [Packaged skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with checklists and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mandatory workflow gates for tests, git checkpoints, verification, delegated follow-up, and session handoff.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
