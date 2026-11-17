## Description:

Generates images and videos using MuleRouter or MuleRun multimodal APIs for text-to-image, image-to-image, text-to-video, image-to-video, and video editing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misaka43fd](https://clawhub.ai/user/misaka43fd)

### License/Terms of Use:


## Use Case:

Developers and creative automation users use this skill to configure MuleRouter or MuleRun API access, inspect supported model parameters, and run image or video generation and editing tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media inputs, and the MuleRouter API key are sent to MuleRouter, MuleRun, or a configured custom endpoint.

Mitigation: Use the skill only in trusted workspaces, keep API keys out of source control, and avoid custom base URLs unless you control the endpoint.

Risk: Local image path handling can upload explicit files to the configured API service.

Mitigation: Pass only intentional, non-sensitive image files and review image paths before execution.

Risk: A local .env file can influence API credentials or endpoint selection.

Mitigation: Run the skill from an expected directory and avoid directories containing untrusted .env files.

## Reference(s):

- [MuleRouter Skill page](https://clawhub.ai/misaka43fd/skills/mulerouter-skills)
- [MuleRouter API Reference](references/REFERENCE.md)
- [Model Reference](references/MODELS.md)
- [MuleRouter API endpoint](https://api.mulerouter.ai)
- [MuleRun API endpoint](https://api.mulerun.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands, configuration examples, task status text, and optional JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is returned as image or video URLs from asynchronous API tasks.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
