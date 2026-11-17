## Description:

Helps agents use the Kie AI API to generate professional images with Google Nano Banana Pro, including prompt shaping, parameter selection, task submission, status checks, and webhook guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to prepare Kie AI Nano Banana Pro image-generation requests, choose aspect ratio, resolution, output format, reference images, and understand task completion flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and callback URLs may be sent to Kie AI or a configured callback endpoint.

Mitigation: Use approved prompts and images, store API keys with a trusted secret mechanism, and configure only HTTPS callback endpoints that the user controls and can verify.

Risk: Generated image requests depend on a third-party API and may be affected by authentication, quota, validation, rate-limit, or service errors.

Mitigation: Handle documented API responses and task states, check credentials and account balance, respect rate limits, and retry or escalate failures according to Kie AI guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/kie-nano-banana-pro)
- [Kie AI Google Pro Image-to-Image API documentation](https://docs.kie.ai/market/google/pro-image-to-image)
- [Kie AI task detail documentation](https://docs.kie.ai/common-api/get-task-detail)
- [Kie AI webhook verification documentation](https://docs.kie.ai/common-api/webhook-verification)
- [Kie AI API key management](https://kie.ai/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, configuration, guidance]

**Output Format:** [Markdown status summaries and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, image-generation parameters, prompt suggestions, status-check guidance, and webhook setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
