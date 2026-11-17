## Description:

Operate the installed pixiv CLI to search works and users, reverse-search images with SauceNAO or ascii2d, inspect Pixiv references, read feeds and rankings, and perform explicitly authorized bookmark, follow, comment, account, or download actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flanchanxwo](https://clawhub.ai/user/flanchanxwo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users invoke Pixiv discovery, account, and download operations through the installed pixiv CLI. The skill guides scoped commands and credential handling, and requires explicit authorization for account changes and downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refresh tokens and exported credential bundles are plaintext secrets.

Mitigation: Keep tokens and bundles out of chat, logs, and diagnostics; use private destinations or a direct consumer pipeline for exports.

Risk: Account changes and downloads can affect user data or write files.

Mitigation: Require explicit authorization for the exact account action, target, and download destination.

Risk: Reverse image search may upload the selected image to third-party providers.

Mitigation: Upload only images the user has authorized for sharing with those providers.

Risk: MCP access or remote login can expose account capabilities to an untrusted client or connection.

Mitigation: Use HTTPS for remote login and grant MCP access only to trusted clients.

## Reference(s):

- [Authentication guide](artifact/references/auth.md)
- [Discovery guide](artifact/references/discover.md)
- [Download guide](artifact/references/download.md)
- [Installation guide](artifact/references/install.md)
- [MCP guide](artifact/references/mcp.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)
- [Pixiv CLI project](https://github.com/FlanChanXwO/pixiv-cli)
- [ClawHub skill release](https://clawhub.ai/flanchanxwo/skills/pixiv-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON or NDJSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are scoped to the requested Pixiv operation; account changes and downloads require explicit authorization.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
