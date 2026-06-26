## Description: <br>
Generates and edits images and videos through MuleRouter or MuleRun multimodal APIs, covering text-to-image, image-to-image, text-to-video, image-to-video, VACE video editing, and keyframe interpolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Misaka43fd](https://clawhub.ai/user/Misaka43fd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure MuleRouter or MuleRun credentials, inspect supported model parameters, and run CLI scripts that generate, edit, or transform images and videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and local image files supplied as image inputs are sent to MuleRouter, MuleRun, or the configured base URL. <br>
Mitigation: Use non-sensitive prompts and media, avoid confidential local file paths, and review what will be sent before running generation or editing commands. <br>
Risk: A custom endpoint configuration can send API keys and request payloads to an unintended service. <br>
Mitigation: Verify MULEROUTER_BASE_URL or MULEROUTER_SITE before use and use a dedicated API key for this skill. <br>


## Reference(s): <br>
- [MuleRouter API Reference](references/REFERENCE.md) <br>
- [Model Reference](references/MODELS.md) <br>
- [Mulerouter ClawHub listing](https://clawhub.ai/Misaka43fd/mulerouter-skills) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; CLI scripts return plain text or JSON containing task status and generated media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce image or video result URLs after asynchronous task polling.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; pyproject.toml declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
