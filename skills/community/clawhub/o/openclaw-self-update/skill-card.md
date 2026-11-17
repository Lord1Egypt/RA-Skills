## Description:

Update npm-installed OpenClaw instances to the latest version with version checks, global npm install commands, gateway restart, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jchen0824](https://clawhub.ai/user/jchen0824)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check, update, restart, and verify npm-installed OpenClaw deployments. It provides manual update commands and an automated shell script for routine OpenClaw maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update path installs the unpinned latest OpenClaw npm release, so the exact package version can change between review and execution.

Mitigation: Prefer an exact OpenClaw version and verify the npm release source before running the script or copied commands.

Risk: Restarting the OpenClaw gateway can interrupt active work or services.

Mitigation: Run during a maintenance window, verify gateway health afterward, and keep a rollback plan available.

Risk: Using elevated permissions for a global npm install expands the impact of a compromised or incorrect package.

Mitigation: Avoid sudo npm install where possible and use a controlled Node.js or package-management environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, code, guidance]

**Output Format:** [Markdown with bash command blocks and a shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands update the global OpenClaw npm package, restart the gateway, and verify the resulting version.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
