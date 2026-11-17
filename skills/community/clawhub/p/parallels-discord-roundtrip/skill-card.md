## Description:

Run macOS Parallels smoke with Discord send, host verification, host reply, and guest readback proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to verify two-way Discord messaging from a macOS guest running in Parallels, including host-side confirmation and guest readback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A VM recovery step may discard suspended state and lose unsaved work.

Mitigation: Confirm the VM and snapshot are disposable, or preserve a recoverable copy before changing snapshot state.

Risk: A Discord-configured VM left running after the smoke may continue reading or posting messages.

Mitigation: Shut down the guest after successful proof, and stop it manually after ad-hoc checks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/parallels-discord-roundtrip)

## Skill Output:

**Output Type(s):** [Shell commands, Test results, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and pass criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A machine-readable summary can be requested with --json.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
