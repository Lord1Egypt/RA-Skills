## Description: <br>
Deploy, secure, and operate MinIO object storage using mc workflows, policy controls, replication, and incident-safe runbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, storage administrators, and reliability engineers use this skill to plan and operate MinIO deployments, bucket lifecycle controls, access policies, replication, hardening, and incident recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide sensitive storage administration actions, including bucket deletion, policy replacement, retention changes, and replication updates. <br>
Mitigation: Require explicit user approval before mutating actions and verify endpoint alias, environment, scope, expected impact, and rollback path before execution. <br>
Risk: Stored operational context may become stale or accidentally include sensitive information. <br>
Mitigation: Keep ~/minio/ notes free of credentials, save only reusable operational context, and review stored assumptions before relying on them. <br>
Risk: Commands may target the wrong MinIO environment or appear successful without validating object and access behavior. <br>
Mitigation: Use read-then-write workflows, capture pre-change state, and confirm results with independent data-path and auth-path checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/minio) <br>
- [Skill homepage](https://clawic.com/skills/minio) <br>
- [MinIO documentation](https://min.io/docs) <br>
- [Setup - MinIO Operations](setup.md) <br>
- [Deployment Patterns - MinIO](deployment-patterns.md) <br>
- [mc Operations Playbook](mc-operations.md) <br>
- [Hardening and Disaster Recovery](hardening-dr.md) <br>
- [Memory Template - MinIO Operations](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MinIO client commands, configuration steps, approval gates, and verification checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
