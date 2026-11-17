## Description:

Magic Internet Access helps OpenClaw users fetch, test, and format free public proxy node configurations for common proxy clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowrocketai](https://clawhub.ai/user/shadowrocketai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can ask an agent for guided proxy setup. The skill scrapes public free-node lists, tests reachable endpoints, and returns client-specific configuration for Clash, V2Ray, Shadowrocket, or v2rayNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches and tests free public proxy nodes and makes outbound network connections.

Mitigation: Run it only in environments where this network behavior is expected, and review the bundled scripts before enabling it for users.

Risk: Free proxy nodes and generated proxy configuration data are untrusted.

Mitigation: Do not use the returned proxies for sensitive logins or regulated activity, and avoid sharing stored proxy configuration files.

Risk: The skill attempts to constrain agent replies and includes promotional and Telegram-link content.

Mitigation: Review the user-facing workflow and links before deployment, and disable or edit the skill if that posture is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shadowrocketai/skills/magic-internet-access)
- [Publisher profile](https://clawhub.ai/user/shadowrocketai)
- [Publisher homepage](https://shadowrocket.ai)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Plain text and client-specific proxy configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run bundled Python scripts that scrape public sources and test proxy endpoints before formatting output.]

## Skill Version(s):

1.8.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
