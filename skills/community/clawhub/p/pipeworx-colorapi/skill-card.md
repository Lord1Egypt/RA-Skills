## Description: <br>
Color identification, scheme generation, and format conversion via TheColorAPI for hex, RGB, HSL, and CMYK workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and accessibility reviewers use this skill to identify named colors, generate harmonious palettes, convert between color formats, and inspect contrast information for design and brand workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VirusTotal telemetry was pending in the security evidence. <br>
Mitigation: Wait for completed multi-engine scan results before relying on the skill in stricter environments. <br>
Risk: The skill relies on a remote ColorAPI/MCP endpoint, so availability and returned color data depend on that service. <br>
Mitigation: Verify service availability and review returned color or contrast data before using it for production design or accessibility decisions. <br>
Risk: The setup example installs mcp-remote with the latest tag at runtime. <br>
Mitigation: Pin mcp-remote to a reviewed version in managed or production environments. <br>


## Reference(s): <br>
- [Pipeworx ColorAPI homepage](https://pipeworx.io/packs/colorapi) <br>
- [Pipeworx ColorAPI MCP endpoint](https://gateway.pipeworx.io/colorapi/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Structured color data with JSON configuration and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces color names, hex/RGB/HSL/CMYK values, palette entries, and contrast information.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
