## Description: <br>
Generate professional AI product photos with ProductAI.photo for ecommerce, marketing, catalogs, and campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shapes](https://clawhub.ai/user/Shapes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, ecommerce teams, marketers, and designers use this skill to configure ProductAI.photo and generate, upscale, or batch-create product images from supplied image URLs and prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ProductAI API keys are sensitive credentials. <br>
Mitigation: Enter API keys through the local setup script or a secret manager instead of pasting them into chat, logs, or shared files. <br>
Risk: Product image URLs, prompts, and job data are sent to ProductAI.photo, a third-party service. <br>
Mitigation: Avoid confidential or regulated product assets unless their use with ProductAI.photo has been approved. <br>
Risk: Batch generation and upscaling can consume paid ProductAI tokens. <br>
Mitigation: Review model costs before running jobs and monitor token usage, especially for batch workflows and upscaling. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Shapes/productai-skill) <br>
- [ProductAI Website](https://www.productai.photo) <br>
- [API Reference](references/API.md) <br>
- [Integration Guide](references/INTEGRATION_GUIDE.md) <br>
- [Quick Start Guide](QUICKSTART.md) <br>
- [Security Guidance](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local image files and a local config.json; ProductAI generation, batch jobs, and upscaling can consume paid tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
