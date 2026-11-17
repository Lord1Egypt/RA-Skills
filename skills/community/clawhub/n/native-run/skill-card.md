## Description:

Execute native commands on the local Windows machine and return their output to OpenClaw for automation and testing purposes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sadikjarvis](https://clawhub.ai/user/sadikjarvis)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to run local Windows commands through an OpenClaw gateway and receive command output for testing, automation, and local tooling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local command execution can allow triggered commands to run on the local gateway machine and expose their output.

Mitigation: Install only in a tightly trusted, isolated environment and restrict skill triggering to trusted users and systems.

Risk: Weakly controlled access to the localhost runner, including shared embedded credentials, may let a reachable caller run local commands.

Mitigation: Prefer explicit command allowlists, per-use confirmation, generated per-install credentials, sandboxing, and audit logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sadikjarvis/skills/native-run)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text command output or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns output from commands executed on the local Windows gateway machine.]

## Skill Version(s):

0.0.1 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
