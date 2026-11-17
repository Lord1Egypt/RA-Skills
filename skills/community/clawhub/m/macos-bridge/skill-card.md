## Description:

Bridge Mac-owned tools like imsg, remindctl, memo, things, and peekaboo onto a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN, enabled-channel auto-discovery, and OpenClaw config fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to expose macOS-backed tools on a Linux gateway through explicit same-LAN SSH wrappers. It helps map enabled OpenClaw channels to Mac-owned binaries, install wrapper commands, and verify the resulting bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated SSH destinations can be persisted into executable wrappers if host mappings or OpenClaw remoteHost values are influenced.

Mitigation: Install only when you control the OpenClaw config and all host mappings; review every --map, --default-host, and remoteHost value before installation, and reject values that start with '-' or contain SSH options.

## Reference(s):

- [Skill Readiness](references/skill-readiness.md)
- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/skills/macos-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces install and verification guidance for Linux-side SSH wrappers that call macOS-owned tools.]

## Skill Version(s):

0.6.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
