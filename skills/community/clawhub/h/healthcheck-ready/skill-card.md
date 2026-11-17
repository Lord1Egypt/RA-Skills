## Description:

Performs a quick risk posture check on the host and provides a concise snapshot of OpenClaw security and readiness status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankou11](https://clawhub.ai/user/ankou11)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a lightweight local readiness snapshot for disk, CPU, memory, key services, and OpenClaw process presence. It is best suited for quick status checks and starter customization rather than authoritative hardening proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health-check output can be overbroad or imprecise and should not be treated as proof that OpenClaw is patched or hardened.

Mitigation: Use it only as a lightweight local status snapshot and confirm patching or hardening with authoritative controls before making security decisions.

Risk: The output may expose process names, usernames, service presence, and local resource details.

Mitigation: Avoid sharing the output in public or untrusted channels and redact environment-specific details when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ankou11/skills/healthcheck-ready)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status report with shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local process names, usernames, disk, CPU, memory, and service presence signals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
