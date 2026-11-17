## Description:

Search 200,000+ open-source icons across 150+ collections — Material Design, Font Awesome, Heroicons, Lucide, and more

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to search icon collections, retrieve SVG data, compare icon styles, and build icon picker workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup automatically runs an unpinned third-party npm package.

Mitigation: Pin mcp-remote to a reviewed exact version and avoid automatic -y installs where possible.

Risk: Using the skill depends on a remote MCP service and an npm-based launcher.

Mitigation: Install only if that trust model is acceptable and run the MCP client with minimal file, credential, and environment access.

## Reference(s):

- [Pipeworx Iconify homepage](https://pipeworx.io/packs/iconify)
- [Pipeworx Iconify MCP endpoint](https://gateway.pipeworx.io/iconify/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-iconify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns icon names, collection prefixes, SVG data, collection metadata, MCP configuration, and curl examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
