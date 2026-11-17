## Description:

Detect what media the user is playing on Windows (Spotify, VLC, Chrome, etc.) via SMTC, and optionally display it on Discord via Rich Presence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isam-ahmed0](https://clawhub.ai/user/isam-ahmed0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Goodrp to query current Windows media playback and manage Discord Rich Presence, including manual, automatic, and overridden status display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust a local GoodRP executable that can read current media activity and publish it to Discord.

Mitigation: Install only if you trust the GoodRP upstream executable and can verify the release yourself.

Risk: Auto-show can share future media activity on Discord automatically.

Mitigation: Enable auto-show only when that ongoing disclosure is intended, and clear presence when media should not be shared.

Risk: The optional HTTP API can expose local control of GoodRP if enabled outside the intended local-only use.

Mitigation: Avoid enabling the HTTP API unless needed and keep it bound to localhost.

## Reference(s):

- [ClawHub Goodrp release page](https://clawhub.ai/isam-ahmed0/skills/goodrp-skill)
- [Server-resolved GitHub import](https://github.com/isam-ahmed0/GoodRP-Skill)
- [GoodRP releases](https://github.com/isam-ahmed0/GoodRP/releases)
- [GoodRP bundled skill source](https://github.com/isam-ahmed0/GoodRP/tree/main/skills/goodrp)
- [Discord Developer Applications](https://discord.com/developers/applications)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls that read current media state and update Discord presence when GoodRP is installed and running.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter metadata version 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
