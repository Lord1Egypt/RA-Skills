## Description:

AGI指令迭代与执行监督工具，将模糊指令拆解为可执行任务，设置奖惩机制，校验执行结果，并在不合格时重写指令形成闭环。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengxiangshu666](https://clawhub.ai/user/mengxiangshu666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn vague AGI instructions into measurable subtasks, scoring rules, verification decisions, and rewritten prompts for iterative execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task prompts may be saved locally under ~/.hermes.

Mitigation: Do not use the skill with sensitive instructions unless local task storage is acceptable.

Risk: The scoring tools have unsafe input handling that could execute commands or overwrite writable JSON files.

Mitigation: Avoid invoking score.sh or the Python score command on untrusted values until numeric validation and task-file path restrictions are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengxiangshu666/skills/hermes-agi-supervisor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON task or scoring records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local task JSON files under ~/.hermes when the included scripts are invoked.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
