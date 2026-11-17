## Description:

Harden OpenClaw workspaces and local OpenClaw configuration by running security audits, checking workspace hygiene, scanning for secrets, applying explicit safe fixes, and planning config.patch hardening changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtaava](https://clawhub.ai/user/virtaava)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to assess and harden an OpenClaw workspace and local ~/.openclaw configuration through audits, hygiene checks, explicit fix commands, and reviewed config.patch plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workspace check path can execute workspace-controlled shell code.

Mitigation: Run workspace checks only on trusted repositories, or remove the repo-local audit execution and make it explicitly opt-in before use on untrusted repositories.

Risk: File traversal can reach outside the intended scope.

Mitigation: Add symlink containment and target-root validation before using fix mode or allowing broad filesystem writes.

Risk: The skill can modify the workspace and ~/.openclaw when fix or apply-config modes are invoked.

Mitigation: Use read-only check and plan modes first, review generated patches and findings, and invoke modifying commands only after confirming the target paths and changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/virtaava/skills/openclaw-hardener)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command output, with optional JSON findings and config.patch JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check mode is read-only by default; fix and apply-config modes require explicit user action.]

## Skill Version(s):

0.1.2 (source: openclaw-skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
