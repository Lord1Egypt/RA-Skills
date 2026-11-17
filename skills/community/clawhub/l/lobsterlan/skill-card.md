## Description:

LobsterLAN lets OpenClaw agents communicate on a local network for synchronous questions, asynchronous task delegation, and peer status checks using configured peer addresses and tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielithomas](https://clawhub.ai/user/danielithomas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let OpenClaw agents ask peer agents questions, delegate longer tasks asynchronously, and check peer reachability on controlled local networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured peer requests can carry agent messages and reusable bearer tokens over plaintext HTTP.

Mitigation: Use localhost, SSH tunnels, or TLS-protected endpoints; keep peers.json private and rotate narrowly scoped tokens.

Risk: Prompts or delegated tasks may expose sensitive operational information to peer agents.

Mitigation: Install only for trusted peer agents and avoid sending sensitive prompts or tasks across direct LAN HTTP.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielithomas/skills/lobsterlan)
- [Publisher profile](https://clawhub.ai/user/danielithomas)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl-based HTTP requests to configured peers and prints command output or status text.]

## Skill Version(s):

1.0.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
