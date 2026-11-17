## Description:

Use when turning development work into Feishu/Lark tasks through lark-cli or feishu-cli, including task lists, bug queues, status updates, blocked work, next actions, or task-linked Dev Hub records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn implementation work, bug follow-up, review state, and verification needs into Lark/Feishu task workflows and durable Dev Hub records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may update task statuses or create durable Base records using the configured Lark/Feishu account.

Mitigation: Use an account with appropriate workspace permissions and review intended task or Base updates before applying them.

Risk: Bug work can be closed without durable verification evidence if the workflow is applied loosely.

Mitigation: Record verification results in a durable task-linked location before closing bug tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afengzi/skills/lark-cli-devhub-taskflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline CLI command references and task status labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires lark-cli; may defer exact command syntax and task GUID handling to the official lark-task skill when installed.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
