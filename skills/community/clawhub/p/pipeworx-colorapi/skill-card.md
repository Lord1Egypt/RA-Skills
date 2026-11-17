## Description:

Color identification, scheme generation, and format conversion via TheColorAPI - hex, RGB, HSL, and CMYK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to identify named colors, generate harmonious palettes, convert between hex, RGB, HSL, and CMYK formats, and inspect contrast information for design and accessibility work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned npm package with automatic approval, giving mutable third-party code local execution authority.

Mitigation: Review setup before installing, prefer a pinned and audited mcp-remote version, run it in a constrained environment, and avoid exposing sensitive environment variables or project secrets to the MCP process.

## Reference(s):

- [Pipeworx ColorAPI pack homepage](https://pipeworx.io/packs/colorapi)
- [Pipeworx ColorAPI MCP endpoint](https://gateway.pipeworx.io/colorapi/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-colorapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include color names, hex, RGB, HSL, CMYK, contrast information, palette entries, and MCP setup snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
