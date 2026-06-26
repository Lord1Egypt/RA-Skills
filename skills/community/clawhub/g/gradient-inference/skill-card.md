## Description: <br>
Community skill for DigitalOcean Gradient AI Serverless Inference that discovers models and pricing, runs chat completions or the Responses API with prompt caching, and generates images through OpenAI-compatible endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simondelorean](https://clawhub.ai/user/simondelorean) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect DigitalOcean Gradient model availability and pricing, send selected prompts to chat or Responses API endpoints, and generate images from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, system messages, and image prompts are sent to DigitalOcean Gradient with the user's API key. <br>
Mitigation: Use a dedicated Gradient key where possible, monitor usage, and avoid sending confidential or regulated content unless DigitalOcean processing is approved. <br>
Risk: Prompt caching can store prompt context for reuse by the provider. <br>
Mitigation: Leave --cache off for confidential or regulated content. <br>


## Reference(s): <br>
- [DigitalOcean Gradient Serverless Inference docs](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/) <br>
- [DigitalOcean Gradient models reference](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/) <br>
- [DigitalOcean Gradient pricing reference](https://docs.digitalocean.com/products/gradient-ai-platform/details/pricing/) <br>
- [ClawHub skill page](https://clawhub.ai/simondelorean/gradient-inference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON-capable CLI output, and generated image files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, GRADIENT_API_KEY, requests>=2.31.0, and beautifulsoup4>=4.12.0 for live pricing lookup.] <br>

## Skill Version(s): <br>
0.1.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
