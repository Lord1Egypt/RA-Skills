## Description: <br>
Generate OpenClaw model inventory and model-card images from openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdsdsdff](https://clawhub.ai/user/sdsdsdff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw model configuration, list configured providers and defaults, check fallback chains, and optionally render a shareable model-card image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated text or images can expose model and provider configuration. <br>
Mitigation: Review generated output before sharing and publish only sanitized artifacts. <br>
Risk: Rendering untrusted OpenClaw configuration values into an image can carry unsafe or misleading config-derived content into the generated artifact. <br>
Mitigation: Use an explicit --config path and render only configuration files from trusted sources. <br>


## Reference(s): <br>
- [OpenClaw Model Card on ClawHub](https://clawhub.ai/sdsdsdff/openclaw-model-card) <br>
- [Publisher profile](https://clawhub.ai/user/sdsdsdff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Terminal text output, Markdown tables, and optional PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads an OpenClaw JSON configuration and can perform consistency checks for missing model references, alias conflicts, and suspicious context-window values.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
