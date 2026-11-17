## Description:

OpenClaw Color Palette provides MCP-accessible color tools for generating harmonious palettes, checking WCAG contrast, converting color formats, simulating color vision deficiencies, and extracting dominant colors from images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd)

### License/Terms of Use:


## Use Case:

Developers, designers, and agents use this skill to generate design palettes, evaluate color accessibility, convert color values, simulate color vision deficiencies, and extract brand colors from images or logos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Color values and submitted image data are sent to a remote MCP service for processing.

Mitigation: Avoid sending private or sensitive images unless the service operator is trusted.

Risk: Broad color-related trigger phrases may activate the skill when a request does not require remote color processing.

Mitigation: Prefer explicit color-related requests and review tool calls before submitting data.

Risk: Color vision deficiency simulation is illustrative and not clinically calibrated.

Mitigation: Do not use simulation output for medical diagnosis; consult appropriate clinical expertise for medical questions.

## Reference(s):

- [OpenClaw MCP Servers](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers)
- [OpenClaw Color Palette on ClawHub](https://clawhub.ai/yedanyagamiai-cmd/skills/openclaw-color-palette)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with structured color values, JSON-like tool results, and CSS custom property snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hex, RGB, HSL, HSV, CMYK, CSS named colors, WCAG contrast results, simulated color values, and extracted palette percentages.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
