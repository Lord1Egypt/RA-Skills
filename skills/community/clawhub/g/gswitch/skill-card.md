## Description: <br>
GSwitch coordinates seven OpenClaw engineering roles through a shared workflow for planning, building, reviewing, testing, securing, releasing, and reflecting on software work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garysze77](https://clawhub.ai/user/garysze77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use GSwitch to coordinate OpenClaw subagents across product framing, architecture, implementation, design review, code review, QA, security audit, release, and retrospective work. It is intended for multi-agent engineering workflows that need explicit role boundaries and an append-only shared project log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared-memory logging may capture secrets, sensitive findings, or project data. <br>
Mitigation: Keep shared memory in a dedicated project directory, restrict access, and do not store secrets or sensitive findings in shared logs. <br>
Risk: The workflow includes production deployment steps and can proceed from QA to release. <br>
Mitigation: Require explicit human approval before production deployment, destructive changes, or rollback actions. <br>
Risk: Recommended settings allow deep, concurrent, and unbounded agent execution. <br>
Mitigation: Set practical run limits, constrain concurrent subagents, and monitor spawned agent activity for the target environment. <br>


## Reference(s): <br>
- [GSwitch on ClawHub](https://clawhub.ai/garysze77/gswitch) <br>
- [Publisher profile](https://clawhub.ai/user/garysze77) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown role instructions, design documents, review reports, test notes, deployment checklists, code changes, shell commands, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents append structured status notes to a shared daily Markdown log and may hand work to other configured roles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
