## Description:

Community skill for DigitalOcean Gradient AI Serverless Inference that discovers available models and pricing, runs chat completions or Responses API calls with prompt caching, and generates images through an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simondelorean](https://clawhub.ai/user/simondelorean)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect DigitalOcean Gradient model availability and pricing, run text inference, and request image generation from agent workflows. It is intended for users who are comfortable sending selected prompts and a Gradient API key to DigitalOcean.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Gradient API key are sent to DigitalOcean for inference requests.

Mitigation: Use the skill only for prompts you are comfortable sending to DigitalOcean and manage GRADIENT_API_KEY as a sensitive credential.

Risk: Prompt caching can retain selected prompt context with the provider account.

Mitigation: Avoid enabling --cache for sensitive prompts unless retention and account-scoping behavior are acceptable.

Risk: The scanner reports unsafe local file-write behavior in image-saving and pricing-cache code.

Mitigation: Run the skill as a non-privileged user and prefer a sandboxed working directory for image outputs until the path validation, URL download controls, and /tmp cache handling are fixed.

## Reference(s):

- [DigitalOcean Gradient Serverless Inference documentation](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/)
- [DigitalOcean Gradient model reference](https://docs.digitalocean.com/products/gradient-ai-platform/details/models/)
- [DigitalOcean Gradient pricing reference](https://docs.digitalocean.com/products/gradient-ai-platform/details/pricing/)
- [Gradient Inference on ClawHub](https://clawhub.ai/simondelorean/skills/gradient-inference)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or image file outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts require GRADIENT_API_KEY for inference calls; pricing lookup can run without an API key.]

## Skill Version(s):

0.1.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
