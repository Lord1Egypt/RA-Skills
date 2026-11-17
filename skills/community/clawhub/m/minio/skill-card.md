## Description:

Deploy, secure, and operate MinIO object storage using mc workflows, policy controls, replication, and incident-safe runbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, platform engineers, and storage operators use this skill to plan and execute MinIO deployment, bucket lifecycle, access policy, replication, hardening, and incident recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bucket deletion, lifecycle rewrites, policy replacement, retention changes, and replication updates can cause data loss, access lockout, or unintended exposure.

Mitigation: Require explicit user approval, confirm scope and rollback path, capture pre-change state, and verify results through independent read checks.

Risk: Operational notes in ~/minio/ could accidentally retain secrets or raw credentials.

Mitigation: Store only reusable operational context and keep credentials, access keys, tokens, and unrelated personal data out of memory files.

Risk: Commands against the wrong MinIO alias, topology, region, or TLS endpoint can produce misleading results or mutate the wrong environment.

Mitigation: Classify topology first, verify aliases and endpoint trust before writes, and start with read-only mc diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/minio)
- [Official MinIO documentation](https://min.io/docs)
- [Setup guide](setup.md)
- [Deployment patterns](deployment-patterns.md)
- [mc operations playbook](mc-operations.md)
- [Hardening and disaster recovery playbook](hardening-dr.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, operational checklists, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local notes under ~/minio/ and requires user approval before destructive or privilege-changing storage operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
