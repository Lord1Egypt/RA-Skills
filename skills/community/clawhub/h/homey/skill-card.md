## Description:

Control Athom Homey smart home devices via local (LAN/VPN) or cloud APIs, including listing and controlling devices, triggering flows, and querying zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxsumrall](https://clawhub.ai/user/maxsumrall)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and automation operators use this skill to let an agent inspect and control Homey smart-home devices, zones, and flows through a local or cloud CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact physical-device actions through Homey, including locks, flows, thermostats, and other state-changing commands.

Mitigation: Require explicit user confirmation before sensitive state changes and prefer exact device or flow IDs over fuzzy names.

Risk: Local discovery and saved HTTP addresses can expose smart-home control paths on untrusted LANs or VPNs.

Mitigation: Use the skill only in trusted environments, prefer secure and verified endpoints where available, and avoid saving discovered HTTP addresses on untrusted networks.

Risk: Homey local API keys and cloud tokens grant access to smart-home data and controls.

Mitigation: Protect tokens as secrets, provide them through secure configuration, and rotate or clear them if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maxsumrall/skills/homey)
- [Homey CLI Documentation](https://maxsumrall.github.io/homeycli/)
- [Homey Developer Tools API Clients](https://tools.developer.homey.app/api/clients)
- [Output Contract](docs/output.md)
- [Command Reference](docs/commands.md)
- [Errors and Exit Codes](docs/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stable JSON output for agent parsing when commands are run with --json.]

## Skill Version(s):

1.1.2 (source: evidence.release.version, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
