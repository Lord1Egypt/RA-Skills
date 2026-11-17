## Description:

Checks a migrated or newly configured agent environment by auditing memory files, skills, tools, dependencies, clones, automation, corpora, backups, and stress-test workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after migration, machine replacement, or new-environment setup to verify that local agent files, skills, tools, dependencies, automation, corpora, clones, and backups are complete and working.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive a broad local audit of agent files, tools, dependencies, automation, backups, and test artifacts.

Mitigation: Confirm the intended workspace paths, backup locations, and temporary output locations before running verification.

Risk: Repair or cleanup actions may restore skills, replace paths, install dependencies, rebuild automation, or delete test artifacts.

Mitigation: Require explicit user approval before any install, restore, rebuild, path replacement, or deletion step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hechunxian/skills/migration-verify)

## Skill Output:

**Output Type(s):** [guidance, shell commands, analysis]

**Output Format:** [Markdown status report with checklist results and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local verification scripts, dependency checks, repair steps, and cleanup of test artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
