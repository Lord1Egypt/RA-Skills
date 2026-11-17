## Description:

Generate images from HTML/CSS templates and capture webpage screenshots via propzapi.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to render Open Graph images, social cards, certificates, invoices, charts, reusable templates, and live webpage screenshots through PropzAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image, template, and screenshot jobs are processed by PropzAPI as a third-party rendering service.

Mitigation: Avoid sending confidential page URLs, private HTML, or sensitive template variables unless that processing is acceptable for the intended use.

Risk: Render and screenshot calls consume PropzAPI credits.

Mitigation: Monitor credit usage and reserve calls for user-requested image generation or webpage capture tasks.

## Reference(s):

- [PropzAPI homepage](https://propzapi.com)
- [PropzAPI documentation](https://propzapi.com/docs)
- [PropzAPI OpenAPI specification](https://api.propzapi.com/openapi.json)
- [PropzAPI MCP server](https://api.propzapi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/paperandbeyond23-gif/skills/propzapi-full)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python dict responses from PropzAPI calls, plus concise Markdown guidance and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROPZAPI_KEY. Image generation and screenshot calls consume PropzAPI credits; template listing and template creation are documented as free.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
