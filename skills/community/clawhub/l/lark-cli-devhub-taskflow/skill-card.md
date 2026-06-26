## Description: <br>
Use when turning development work into Feishu/Lark tasks through lark-cli or feishu-cli, including task lists, bug queues, status updates, blocked work, next actions, or task-linked Dev Hub records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to keep Feishu/Lark task lists, bug queues, status updates, and Dev Hub records aligned during development work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or update Feishu/Lark tasks and Base records in shared business workspaces. <br>
Mitigation: Use it with the intended authenticated CLI account and review task or Base updates before allowing broad workspace changes. <br>
Risk: Task status or bug evidence can become misleading if verification and root-cause details are not recorded durably. <br>
Mitigation: Record verification results and durable Bugfix or AI Run records before closing bug-related tasks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with CLI-oriented task and record updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing lark-cli or feishu-cli setup and authenticated access to the target Feishu/Lark workspace.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
