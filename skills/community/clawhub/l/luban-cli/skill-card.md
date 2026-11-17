## Description:

Development and management of the Luban CLI for MLOps. Use this skill when building or using the Luban CLI to manage experiment environments, training tasks, and online services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guunergooner](https://clawhub.ai/user/guunergooner)

### License/Terms of Use:


## Use Case:

Developers and MLOps engineers use this skill to build or operate a Luban CLI for managing experiment environments, training jobs, and online inference services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resource create, delete, update, and scale commands can affect production workloads, billing, or service availability if applied to the wrong target.

Mitigation: Require clear target identifiers, confirmations or force flags, dry-run modes where practical, and documentation of billing and service availability impact before executing production-impacting commands.

## Reference(s):

- [Luban CLI MLOps Management Guide](references/mlops_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/guunergooner/skills/luban-cli)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI boilerplate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command patterns for env, job, and svc resources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
