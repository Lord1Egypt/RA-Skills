## Description:

Search and read KOLSprite data through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search TikTok creators, videos, products, and shops, extract video captions, and inspect related product signals through KOLSprite MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs the agent to execute downloaded CLI installation code without a separate approval step; the installer's downstream behavior is unverified.

Mitigation: Review and approve the CLI installation separately, and inspect and verify a specific installer version first. Using an already-installed CLI avoids this setup path.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [KOLSprite MCP](https://www.kolsprite.com)
- [KOLSprite API documentation](https://o.kolsprite.com/doc/api.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and its live input schema.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
