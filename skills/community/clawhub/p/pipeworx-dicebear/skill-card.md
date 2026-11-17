## Description:

Generate unique avatar images from seed text across 30+ styles including pixel art, initials, and abstract shapes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to generate deterministic avatar SVG URLs for users, projects, chat participants, and design prototypes without storing generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration uses a mutable npm package version during setup.

Mitigation: Pin and review the MCP bridge package version before deployment, or avoid the npx @latest configuration in managed environments.

Risk: Seed text may be sent to external avatar services.

Mitigation: Use non-sensitive pseudonymous seeds instead of emails, tokens, customer IDs, or confidential strings.

## Reference(s):

- [Pipeworx DiceBear pack](https://pipeworx.io/packs/dicebear)
- [ClawHub Pipeworx dicebear release](https://clawhub.ai/brucegutman/skills/pipeworx-dicebear)
- [Pipeworx DiceBear MCP endpoint](https://gateway.pipeworx.io/dicebear/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON responses containing SVG avatar URLs and style metadata, plus Markdown guidance with curl and MCP configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seed text and avatar style inputs; generated avatars are deterministic for the same seed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
