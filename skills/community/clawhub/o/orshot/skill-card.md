## Description:

Image, PDF and video generation from Orshot templates, through the hosted MCP server (OAuth, no API key) or the REST API. Covers connecting, finding a template and its parameter keys, render options (formats, sizes, Smart Resize, batch, async), dynamic image URLs, utility templates (tweet and website screenshots, charts, mockups), posting a render to connected social accounts, wiring it into n8n, Make, Zapier or cron, and the gotchas that break renders (parameterId keys, page1@ prefixes, public image URLs). Use when: "render my Orshot template", "connect Orshot to Claude", "call the Orshot API", "my modification is ignored", "automate this render in n8n", "screenshot this tweet", "move from Bannerbear to Orshot". One job end to end: load its skill (orshot-blog-images, orshot-pdf-generator, orshot-video-generator, orshot-ad-creative, orshot-carousel, orshot-youtube-thumbnail, orshot-social-media-content or orshot-social-media-scheduler). NOT for template design craft (use orshot-design).

This skill is ready for commercial/non-commercial use.

## Publisher:

[orshot](https://clawhub.ai/user/orshot)

### License/Terms of Use:

MIT

## Use Case:

Developers and content teams use this skill to connect to Orshot, render images, PDFs, and videos from templates, and integrate those renders into existing automation or social publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template data sent for rendering may contain sensitive content, and the security review is incomplete.

Mitigation: Use sample or redacted records for initial tests, and review the data being sent before using real records.

## Reference(s):

- [Orshot agent skills](https://orshot.com/agents/skills)
- [Orshot MCP server setup](https://orshot.com/docs/integrations/mcp-server.md)
- [Render from a studio template](https://orshot.com/docs/api-reference/render-from-studio-template.md)
- [Recurring automation guide](references/recurring-automation.md)
- [Migration guide](references/migration.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.6.2 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
