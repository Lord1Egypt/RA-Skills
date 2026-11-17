## Description:

Let AI agents capture live website screenshots, render HTML/CSS, and populate reusable templates as images or PDFs without managing a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[htmlcsstoimage](https://clawhub.ai/user/htmlcsstoimage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to render HTML/CSS, public webpage captures, PDFs, and HCTI templates through HCTI MCP tools. It is suited for screenshots, social cards, Open Graph images, and other browser-rendered graphics, not for editing or interpreting existing images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested HTML, CSS, URLs, template values, and rendering options are processed by the hosted HCTI service.

Mitigation: Use public or intentionally shared inputs by default, and avoid private pages or credential-bearing requests unless the user explicitly approves sending that data to HCTI.

Risk: Rendering can consume HCTI account credits or incur service costs under the user's plan.

Mitigation: Treat an explicit single-image request or stated batch count as authorization, and clarify ambiguous batch sizes before rendering.

Risk: Creating or updating templates changes the user's HCTI account.

Mitigation: Only perform template mutations when explicitly requested or after user confirmation.

## Reference(s):

- [HTML/CSS to Image](https://htmlcsstoimage.com)
- [HCTI MCP documentation](https://docs.htmlcsstoimage.com/integrations/mcp/)
- [OpenClaw MCP setup](https://docs.openclaw.ai/cli/mcp/registry)
- [ClawHub skill page](https://clawhub.ai/htmlcsstoimage/skills/html-css-to-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return image or PDF asset URLs from HCTI MCP tools after successful rendering.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
