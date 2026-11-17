## Description:

Safely verify and apply OpenClaw upgrades with isolated sidecar checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianchenx](https://clawhub.ai/user/ianchenx)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to verify an OpenClaw target version in an isolated sidecar before applying an upgrade. It supports verify-only checks by default, optional target pinning, platform-specific prerequisites, and an explicit apply step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux workflow can run newly downloaded npm code and perform a global upgrade with broad system privileges.

Mitigation: Prefer a pinned target version, use a user-local Node toolchain, avoid running the full script with sudo, and review the script and npm source before using --apply on production machines.

## Reference(s):

- [OpenClaw Updating Documentation](https://docs.openclaw.ai/install/updating)
- [Linux Guide](references/linux.md)
- [macOS Guide](references/macos.md)
- [ClawHub Skill Page](https://clawhub.ai/ianchenx/skills/openclaw-safe-update)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through verify-only checks, optional version pinning, explicit upgrade application, and failure reporting with log paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
