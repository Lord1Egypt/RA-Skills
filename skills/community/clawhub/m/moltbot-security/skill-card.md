## Description:

Security hardening for AI agents - Moltbot, OpenClaw, Cursor, Claude. Lock down gateway, fix permissions, auth, firewalls. Essential for vibe-coding setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit and harden Moltbot, OpenClaw, and related AI-agent gateway setups. It provides guidance for loopback binding, authentication, file permissions, Node.js updates, Tailscale remote access, firewall rules, and SSH hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes copy-paste commands that execute remote installer scripts.

Mitigation: Review installer sources first, prefer vendor package-manager instructions with signed repositories, and verify downloaded installers before execution.

Risk: Some guidance applies privileged system changes such as audit fixes, firewall rules, and SSH configuration edits.

Mitigation: Run non-mutating audit commands before using --fix, confirm each privileged change, and keep console recovery access before applying firewall or SSH changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextfrontierbuilds/skills/moltbot-security)
- [Node.js downloads](https://nodejs.org/)
- [Tailscale installer](https://tailscale.com/install.sh)
- [Referenced gateway exposure research](https://x.com/nickspisak_/status/2016195582180700592)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security checklist and configuration templates]

## Skill Version(s):

1.0.3 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
