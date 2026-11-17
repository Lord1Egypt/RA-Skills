## Description:

Routes community and commercial distributed OceanBase deployment and operations through OBD, including product-form discovery and handoff to cluster management, OBD administration, tenant management, testing, or diagnostics workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceanbase](https://clawhub.ai/user/oceanbase)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, database administrators, and operations engineers use this skill to plan, review, or execute OceanBase distributed deployment and operations tasks through OBD while preserving explicit execution-mode and safety boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically make persistent SSH, package, and database-access changes.

Mitigation: Review operational defaults before installation or execution, run as an unprivileged user where possible, and explicitly provide target hosts and SSH users.

Risk: Default tenant credentials or allowlists may be unsafe on reachable or production environments.

Mitigation: Override tenant password and allowlist defaults before using the skill against any reachable or production environment.

Risk: Automation can affect persistent OceanBase deployments and supporting OBD controller state.

Mitigation: Prefer a pinned or reviewed manual installation path and require concrete target, impact, and acceptance criteria before mutation.

## Reference(s):

- [README](README.md)
- [Operation Contract](references/operation-contract.md)
- [Product and Capability Resolution](references/product-and-capability-resolution.md)
- [Deployment Package Sets](references/deployment-package-sets.md)
- [Completion Criteria](references/completion-criteria.md)
- [Failure Recovery and Evidence](references/failure-recovery-and-evidence.md)
- [Cluster Configuration Deployment](cluster-management/references/config-deployment.md)
- [OBD Mirror and Repositories](obd-administration/references/mirror-and-repositories.md)
- [Tenant Creation](tenant-management/references/tenant-creation.md)
- [Testing Common Workflow](testing-and-benchmark/references/common-workflow.md)
- [Obdiag Workflows](obdiag-diagnostics/references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute host, package, SSH, OBD, and database operations when the user explicitly requests execution.]

## Skill Version(s):

2.0.3 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
