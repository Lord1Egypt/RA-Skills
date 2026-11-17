## Description:

MuleRouter helps agents generate, edit, and transform images and videos through MuleRouter or MuleRun multimodal APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misaka43fd](https://clawhub.ai/user/misaka43fd)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to configure MuleRouter or MuleRun access, inspect supported multimodal models, and run CLI workflows for AI image and video generation, editing, and transformation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured endpoint can receive the user's API key and uploaded media.

Mitigation: Use MULEROUTER_SITE=mulerouter or MULEROUTER_SITE=mulerun, and avoid custom MULEROUTER_BASE_URL values unless the endpoint is fully trusted.

Risk: Local image paths passed to model scripts may be uploaded as media inputs.

Mitigation: Only pass local image files that are intended for upload, and review model parameters before execution.

Risk: The security verdict is suspicious because host and HTTPS validation are not enforced for arbitrary custom base URLs.

Mitigation: Review configuration before installing or running the skill, and restrict execution to trusted endpoints.

## Reference(s):

- [MuleRouter ClawHub skill page](https://clawhub.ai/misaka43fd/skills/mulerouter)
- [misaka43fd publisher profile](https://clawhub.ai/user/misaka43fd)
- [MuleRouter API key page](https://www.mulerouter.ai/app/api-keys?utm_source=github_claude_plugin)
- [MuleRouter API Reference](artifact/references/REFERENCE.md)
- [Model Reference](artifact/references/MODELS.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; model scripts may return plain text or JSON containing generated image or video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MULEROUTER_API_KEY and either MULEROUTER_BASE_URL or MULEROUTER_SITE; uses uv and Python 3.10+.]

## Skill Version(s):

0.1.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
