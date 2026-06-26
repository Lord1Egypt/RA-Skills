## Description: <br>
Generates images and videos using MuleRouter or MuleRun multimodal APIs, including text-to-image, image-to-image, text-to-video, image-to-video, video editing, and keyframe interpolation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Misaka43fd](https://clawhub.ai/user/Misaka43fd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to configure MuleRouter or MuleRun API access, inspect available multimodal models, and run image or video generation and editing jobs from agent-driven shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and selected local image files are sent to MuleRouter or MuleRun for processing. <br>
Mitigation: Use the skill only for content that may be shared with the configured service endpoint, and review media inputs before execution. <br>
Risk: A misconfigured MULEROUTER_BASE_URL can direct API credentials and content to an unintended endpoint. <br>
Mitigation: Keep MULEROUTER_BASE_URL pointed at a trusted MuleRouter or MuleRun endpoint and verify configuration before running generation commands. <br>
Risk: API keys may be exposed through insecure local handling. <br>
Mitigation: Protect any .env file containing MULEROUTER_API_KEY and avoid passing API keys directly on shared command lines. <br>


## Reference(s): <br>
- [MuleRouter ClawHub Skill Page](https://clawhub.ai/Misaka43fd/mulerouter) <br>
- [MuleRouter API Reference](references/REFERENCE.md) <br>
- [Model Reference](references/MODELS.md) <br>
- [MuleRouter API Keys](https://www.mulerouter.ai/app/api-keys?utm_source=github_claude_plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON task results containing generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, uv, MULEROUTER_API_KEY, and either MULEROUTER_BASE_URL or MULEROUTER_SITE; sends prompts, media URLs, and selected local image files to the configured MuleRouter or MuleRun endpoint.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
