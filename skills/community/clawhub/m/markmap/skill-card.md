## Description:

markmap - Render Markdown as interactive SVG mindmaps for converting Markdown documents into mindmaps, generating HTML files via CLI, and navigating mindmap nodes interactively in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to ask an agent for Markmap CLI commands, browser/API examples, and configuration guidance that turn Markdown content into interactive SVG or HTML mindmaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CLI examples may install or run npm packages in the user's Node environment.

Mitigation: Review proposed npm and Markmap commands before execution, and use local project installation or isolated environments when appropriate.

Risk: Generated browser examples may load Markmap assets from public CDNs.

Mitigation: Use the documented offline mode or local asset configuration when external CDN loading is not acceptable.

## Reference(s):

- [Markmap Skill Page](https://clawhub.ai/openlark/skills/markmap)
- [Transformer + Frontmatter](references/transform.md)
- [Markmap Rendering](references/render.md)
- [CLI](references/cli.md)
- [Architecture & Pipeline](references/architecture.md)
- [Type Reference & Common Utilities](references/common-api.md)
- [Plugin System](references/plugins.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline TypeScript, HTML, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm install commands, Markmap CLI usage, browser API snippets, frontmatter options, plugin examples, and offline/CDN asset guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
