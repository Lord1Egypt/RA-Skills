## Description:

Install and configure PeonPing with an opinionated default Orc Peon voice so completion alerts work immediately with minimal user friction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sal-jim](https://clawhub.ai/user/sal-jim)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to install, configure, verify, customize, and troubleshoot PeonPing completion sounds for coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback installer pipes an unverified remote shell script directly into bash.

Mitigation: Prefer the Homebrew install path, or require a pinned and verifiable installer with explicit user approval before running downloaded code.

## Reference(s):

- [PeonPing Website](https://peonping.com)
- [PeonPing GitHub Repository](https://github.com/PeonPing/peon-ping)
- [PeonPing Upstream README](https://raw.githubusercontent.com/PeonPing/peon-ping/main/README.md)
- [ClawHub Skill Page](https://clawhub.ai/sal-jim/skills/peon-ping-openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, setup, pack selection, notification, preview, status, and recovery commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
