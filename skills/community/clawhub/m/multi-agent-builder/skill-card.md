## Description: <br>
Builds reusable OpenClaw multi-agent teams from a user goal, including role analysis, agent creation planning, collaboration protocols, handoff flows, and channel-binding checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzgogo](https://clawhub.ai/user/gzgogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to design, materialize, validate, and hand off reusable multi-agent teams with explicit role contracts, collaboration rules, provisioning plans, and channel-binding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw configuration changes, including agent entries, workspaces, permissions, and channel bindings. <br>
Mitigation: Require a dry run or manual review of the exact openclaw.json diff, workspace paths, generated agent IDs, permissions, and channel binding before execution. <br>
Risk: Generated agents may receive broader tool access than their roles require. <br>
Mitigation: Change generated agents from full tool access to role-specific least privilege before using the team. <br>
Risk: Optional dependency or skill installation can occur with too little per-change user control. <br>
Mitigation: Do not allow automatic optional skill installs; review and approve each dependency or skill installation separately. <br>


## Reference(s): <br>
- [Create Playbook](artifact/references/create-playbook.md) <br>
- [Collaboration Protocol](artifact/references/collaboration-protocol.md) <br>
- [Capability Matrix](artifact/references/capability-matrix.md) <br>
- [Permission Profiles](artifact/references/permission-profiles.md) <br>
- [Provisioning Playbook](artifact/references/provisioning-playbook.md) <br>
- [Channel Binding Blueprints](artifact/references/channel-binding-blueprints.md) <br>
- [Materialization Checklist](artifact/references/materialization-checklist.md) <br>
- [Config Materialization Checklist](artifact/references/config-materialization-checklist.md) <br>
- [Security Report Schema](artifact/references/security-report-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown handoff reports, generated role files, JSON command output, and OpenClaw configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors the user's language and includes role rosters, agent contracts, collaboration flow, provisioning requirements, channel-binding checklist, validation status, and smoke-test prompt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
