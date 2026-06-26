## Description: <br>
Use Lux3D to generate 3D models from images or text, or perform material repaint for international users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violalulu](https://clawhub.ai/user/violalulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and artists use this skill to create downloadable 3D assets from images or text prompts, or to regenerate materials for an existing GLB model using Lux3D's remote API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, mesh URLs, and the Lux3D API key are sent to the configured Lux3D service. <br>
Mitigation: Use the skill only with a trusted Lux3D endpoint and avoid submitting confidential designs or private model URLs unless Lux3D's data-handling terms are acceptable. <br>
Risk: LUX3D_BASE_URL or --base-url can redirect requests, including credentials and submitted assets, to another server. <br>
Mitigation: Leave the default endpoint in place or verify any custom base URL before use. <br>
Risk: Generated model download links are time-limited. <br>
Mitigation: Download generated assets promptly after task completion. <br>


## Reference(s): <br>
- [Lux3D Website](https://lux3d.aholo3d.com/) <br>
- [Lux3D API Key Application](https://labs.aholo3d.com/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/violalulu/lux3d) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Code, Guidance] <br>
**Output Format:** [Downloaded 3D model files such as ZIP, GLB, or USDZ, with Python return values and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LUX3D_API_KEY and sends selected prompts, images, mesh URLs, and generation requests to the configured Lux3D service.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
