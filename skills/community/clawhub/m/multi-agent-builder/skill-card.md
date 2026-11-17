## Description:

Builds reusable OpenClaw multi-agent teams from a user goal, including role analysis, role confirmation, agent contracts, collaboration protocol, handoff flow, and channel-binding checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzgogo](https://clawhub.ai/user/gzgogo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to turn a goal into a confirmed multi-agent team with defined roles, collaboration rules, provisioning requirements, generated role files, and channel-binding plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change OpenClaw configuration and grant broad agent powers.

Mitigation: Require a dry run, review exact configuration diffs, restrict generated agents to least-privilege profiles, and validate team and role IDs before applying changes.

Risk: The skill can install other skills during provisioning.

Mitigation: Approve each dependency install, avoid optional third-party skills by default, and block high-risk or extreme-risk dependencies for review.

Risk: Channel or bot binding can introduce external effects or credential exposure.

Mitigation: Require explicit confirmation for channel credentials and irreversible external effects, and validate account, binding, and routing settings before declaring the team ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gzgogo/skills/multi-agent-builder)
- [Role Discovery Dialog Flow](references/dialog-flow.md)
- [Role Catalog](references/role-catalog.md)
- [Collaboration Protocol](references/collaboration-protocol.md)
- [Create Playbook](references/create-playbook.md)
- [Capability Matrix](references/capability-matrix.md)
- [Permission Profiles](references/permission-profiles.md)
- [Provisioning Playbook](references/provisioning-playbook.md)
- [Config Materialization Checklist](references/config-materialization-checklist.md)
- [Post-Creation Materialization Checklist](references/materialization-checklist.md)
- [Channel Binding Blueprints](references/channel-binding-blueprints.md)
- [Security Report Schema](references/security-report-schema.md)
- [Failure Modes and Recovery Playbook](references/failure-modes.md)
- [Final Deliverable Sample](references/final-deliverable-sample.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON report blocks, shell commands, and generated OpenClaw configuration and role files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw agent configuration, role workspaces, shared directories, and channel binding plans after role confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
