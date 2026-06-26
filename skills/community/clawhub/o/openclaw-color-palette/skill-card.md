## Description: <br>
Design-grade color processing suite for generating harmonious palettes, checking WCAG 2.1 AA/AAA contrast, converting color formats, simulating color vision deficiencies, and extracting dominant colors from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and agents use this skill to create color palettes, verify contrast accessibility, convert color formats, simulate color vision deficiency views, and extract brand colors from images or logos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Color values, image URLs, screenshots, logos, or base64 image data may be sent to the disclosed remote MCP service for processing. <br>
Mitigation: Avoid sensitive or proprietary visuals unless you trust the provider and its no-storage claims; use non-sensitive assets for routine palette work. <br>
Risk: Image extraction depends on remote processing and documented size constraints. <br>
Mitigation: Resize or compress images before submission, especially when extracting palettes from screenshots, logos, or large artwork. <br>
Risk: Color vision deficiency simulation and contrast checks can inform accessibility work but do not replace full accessibility review. <br>
Mitigation: Use the generated results as design guidance and validate final interfaces with broader accessibility checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yedanyagamiai-cmd/openclaw-color-palette) <br>
- [Project homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers) <br>
- [Color Palette MCP endpoint](https://color-palette-mcp.yagami8095.workers.dev/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration and structured color results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces palettes, conversions, WCAG contrast checks, color vision deficiency simulations, and dominant image colors; image and color inputs may be sent to the disclosed remote MCP service.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
