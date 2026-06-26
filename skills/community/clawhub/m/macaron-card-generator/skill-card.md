## Description: <br>
Generate beautiful macaron-color cartoon illustration-style card images from text content, including book recommendation, concept, quote, and comparison cards across multiple aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn structured text into pastel cartoon-style card artwork, then render the generated HTML as a PNG image for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided card fields are rendered in a browser, so untrusted HTML or script-like content can affect the generated output. <br>
Mitigation: Use trusted text, or sanitize and escape card fields before rendering HTML or taking a browser screenshot. <br>
Risk: Broad trigger phrases can activate the skill for generic image or card requests. <br>
Mitigation: Confirm the user wants a macaron-style card and identify the card type, content, and aspect ratio before running the generator. <br>


## Reference(s): <br>
- [Macaron Card Design Reference](references/design_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [HTML file rendered to PNG, with JSON input and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports book, concept, quote, and comparison card types with 1:1, 3:4, 4:3, 9:16, 16:9, and 2:3 aspect ratios.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
