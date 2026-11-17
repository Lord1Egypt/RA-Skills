## Description:

Identifies and helps resolve common OpenClaw AgentSkill issues, including ClawHub installation failures, hardcoded paths, missing or poorly documented dependencies, helper script problems, and script or API integration errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to debug, audit, and validate OpenClaw AgentSkills that fail to install, run, resolve dependencies, use portable paths, or integrate cleanly with OpenClaw APIs and telemetry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled hardcoded-path audit script can mishandle an untrusted target path and allow that target to influence local command execution.

Mitigation: Review the skill before installation, run it only in an isolated workspace when inspecting untrusted directories, and fix scripts/check-hardcoded-paths.sh to canonicalize the target path and pass rg options before a -- terminator.

Risk: Portuguese-only documentation may reduce usability for non-Portuguese users.

Mitigation: Provide English documentation or confirm that intended users can work effectively with the Portuguese workflow and references.

## Reference(s):

- [Common OpenClaw AgentSkill Issues](references/common-skill-issues.md)
- [OpenClaw AgentSkill Debugging Workflow](references/debug-workflow.md)
- [OpenClaw Skill Debugger on ClawHub](https://clawhub.ai/alessandropcostabr/skills/openclaw-skill-debugger)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with diagnostic steps, shell commands, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce audit findings and proposed fixes for a target skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
