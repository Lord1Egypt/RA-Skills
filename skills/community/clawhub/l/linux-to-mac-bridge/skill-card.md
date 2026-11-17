## Description:

Legacy combined bridge skill for Linux-to-Mac wrapper installs. Prefer the newer split skills `macos-bridge` for Mac-owned CLIs and `homebrew-bridge` for Homebrew-backed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill on a Linux gateway to install and verify stable wrapper commands that execute Mac-owned tools over SSH on trusted local Mac nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe SSH host values from a poisoned config or argument could trigger unintended local command execution during wrapper installation.

Mitigation: Use only trusted OpenClaw config files and explicit trusted host mappings, review mappings before installation, and do not run the installer as root.

Risk: Wrapper targets placed in shared or attacker-writable directories could be replaced or misused.

Mitigation: Install wrappers only into trusted user-controlled directories and verify the generated wrapper pack before using it in automation.

Risk: The bridge depends on trusted same-LAN SSH reachability and Mac node readiness.

Mitigation: Use local network or VLAN Mac hosts only, configure explicit tool ownership, and add Wake-on-LAN maps when Mac nodes may sleep.

## Reference(s):

- [Skill Readiness](references/skill-readiness.md)
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/skills/linux-to-mac-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wrapper installation, ownership mapping, Wake-on-LAN, and verification guidance for a Linux-to-Mac bridge workflow.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
