## Description: <br>
Use when designing, provisioning, searching, or writing Feishu/Lark Base records through lark-cli or feishu-cli for a development knowledge hub, including Projects, Areas, Tasks, Bugfixes, Pitfalls, Playbooks, Decisions, Releases, Artifacts, and AI Runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to provision, search, and write Feishu/Lark Base records that track development knowledge such as projects, tasks, bugfixes, pitfalls, playbooks, decisions, releases, artifacts, and AI run evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Lark/Feishu CLI access could inspect schemas or write records to the wrong Base if credentials or BASE_TOKEN are overbroad. <br>
Mitigation: Scope BASE_TOKEN and related CLI credentials to the intended Base and review proposed write commands before execution. <br>
Risk: Development knowledge records could accidentally include secrets or raw credentials. <br>
Mitigation: Follow the skill's write rule to avoid storing secrets or raw credentials in Base records. <br>
Risk: Failed writes could leave misleading state if receipts are invented or skipped. <br>
Mitigation: Use devhub.py when possible so receipts and outbox behavior remain consistent; leave an outbox item when a write fails. <br>


## Reference(s): <br>
- [Lark CLI Dev Hub Base on ClawHub](https://clawhub.ai/afengzi/lark-cli-devhub-base) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lark-cli and python3; guides schema inspection, provisioning, and record-writing workflows.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
