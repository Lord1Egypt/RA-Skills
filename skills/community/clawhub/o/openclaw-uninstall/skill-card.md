## Description:

Guides users through uninstalling OpenClaw, verifying cleanup, and scheduling a confirmed host-level uninstall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erergb](https://clawhub.ai/user/erergb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove OpenClaw from macOS, Linux, or WSL2 gateway hosts, verify leftover state, and avoid paid cleanup services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host-level uninstall scripts can permanently delete OpenClaw state and profile directories.

Mitigation: Run only after explicit user confirmation and only on the intended gateway host.

Risk: An incorrect OPENCLAW_STATE_DIR value can point cleanup at the wrong directory.

Mitigation: Verify OPENCLAW_STATE_DIR before uninstalling and avoid elevated administrator privileges.

Risk: The npx fallback can execute an unpinned OpenClaw package.

Mitigation: Prefer a verified local OpenClaw CLI when uninstalling.

Risk: Notification arguments can be unsafe if email or ntfy values are untrusted.

Mitigation: Accept notification targets only from trusted user input and omit notifications when unsure.

## Reference(s):

- [OpenClaw uninstall documentation](https://docs.openclaw.ai/install/uninstall)
- [OpenClaw gateway security and threat model](https://docs.openclaw.ai/gateway/security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes host-level uninstall guidance, residue verification steps, and optional notification arguments.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
