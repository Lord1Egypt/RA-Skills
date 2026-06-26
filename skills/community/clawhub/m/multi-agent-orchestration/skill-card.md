## Description: <br>
Orchestrates multi-agent task delegation and workflows with audit logging, checkpoint approvals, and agent learning for coordinated project execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dabruhce](https://clawhub.ai/user/dabruhce) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Colony to route work to specialized OpenClaw agents, run multi-stage workflows, pause at checkpoints for review, and collect audit and learning records across tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background agents can perform broad coding, file, deployment, and operational work. <br>
Mitigation: Use the skill only in repositories and environments where those actions are acceptable, and add human approval gates before deploy, delete, git, SSH, Docker, install, or publish actions. <br>
Risk: Prompts, feedback, global context, audit logs, and memory files may persist sensitive project information. <br>
Mitigation: Avoid entering secrets, regulated data, or sensitive business information into Colony context, feedback, prompts, or memory. <br>
Risk: Notifications can send process status outside the local workspace. <br>
Mitigation: Disable notifications unless needed and configure notification targets deliberately before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dabruhce/multi-agent-orchestration) <br>
- [Colony skill instructions](artifact/SKILL.md) <br>
- [Colony documentation](artifact/COLONY-DOCS.md) <br>
- [Process definitions](artifact/colony/processes.yaml) <br>
- [Agent registry](artifact/colony/agents.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task results, generated files, CLI status output, audit records, memory updates, and configured process artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn background OpenClaw agents and write persistent task, audit, context, and memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
