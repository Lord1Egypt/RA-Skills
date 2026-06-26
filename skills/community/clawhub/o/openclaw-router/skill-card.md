## Description: <br>
Openclaw Router routes AI tasks across local and cloud models to optimize cost, track usage, and support multilingual text and optional vision workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pepsiboy87](https://clawhub.ai/user/pepsiboy87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose between local and configured cloud AI models, track token and cost estimates, manage routing thresholds, and optionally analyze images or screenshots through vision-capable providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect model-provider environment variables and may expose key fragments, endpoints, account details, or model inventory through diagnostics or logs. <br>
Mitigation: Use dedicated test API keys, run first in a non-production environment, review any generated logs or screenshots before sharing, and rotate credentials if fragments are exposed. <br>
Risk: Prompts or images may be routed to configured cloud AI providers, including vision/OCR providers, which can disclose sensitive text, screenshots, or regulated data. <br>
Mitigation: Disable or avoid cloud and vision routes unless needed, review routing configuration before use, and keep sensitive or regulated data out of prompts and images until provider handling is approved. <br>
Risk: Automated model selection and cost estimates can choose an unsuitable provider or produce inaccurate budget expectations. <br>
Mitigation: Review threshold and budget settings, test routing decisions with representative tasks, and require human confirmation before using the recommendations for important workloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pepsiboy87/openclaw-router) <br>
- [Project homepage](https://github.com/pepsiboy87/openclaw-router) <br>
- [README](README.md) <br>
- [Vision guide](docs/VISION_GUIDE.md) <br>
- [Examples](docs/EXAMPLES_en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, YAML configuration examples, and routing result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect environment variables for configured model providers and may send prompts or images to selected cloud AI providers when those routes are enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
