## Description: <br>
Long-Running Agent helps AI agents manage multi-step projects across sessions using persistent project briefs, changelogs, progress tracking, failure records, and continuation protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sleepingzzzz](https://clawhub.ai/user/sleepingzzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, resume, monitor, and pause long-running software projects while preserving context across sessions. It is intended for workflows that need persistent memory in PROJECT.md and CHANGELOG.md files, explicit next actions, failed-method tracking, and Git checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project memory may retain sensitive or stale context in PROJECT.md or CHANGELOG.md. <br>
Mitigation: Use the skill in a dedicated workspace, avoid writing secrets to project memory files, and review those files before resuming work. <br>
Risk: Project initialization and continuation can write or overwrite task files. <br>
Mitigation: Back up existing task folders before initializing and review generated file changes before continuing work. <br>
Risk: Arbitrary path options can direct writes outside the intended task area. <br>
Mitigation: Avoid arbitrary --path values and keep project files under the expected workspace task directory. <br>
Risk: Heartbeat or background continuation can resume work without a fresh prompt. <br>
Mitigation: Enable heartbeat-style automation only when unattended continuation is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sleepingzzzz/long-running-agent) <br>
- [Long-Running Tasks Research](https://www.anthropic.com/research/long-running-tasks) <br>
- [clax Reference Implementation](https://github.com/smsharma/clax) <br>
- [Best Practices](references/best-practices.md) <br>
- [Project Template](references/project-template.md) <br>
- [Changelog Template](references/changelog-template.md) <br>
- [Ralph Loop](references/ralph-loop.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update PROJECT.md, CHANGELOG.md, tests directories, and task files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
