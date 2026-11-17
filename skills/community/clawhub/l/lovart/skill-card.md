## Description:

Integrates with the Lovart.ai API to help agents generate AI designs, images, and videos, including image generation, image editing, video creation, and template workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mendynew](https://clawhub.ai/user/mendynew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to turn design requests into Lovart.ai API calls for product images, marketing assets, logos, short videos, and template-based design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, brand details, and related usage metadata may be sent to Lovart.ai under the user's Lovart account.

Mitigation: Use the skill only when Lovart.ai processing is intended, and avoid submitting confidential product, campaign, or branding material unless third-party processing is approved.

Risk: Broad design-related trigger wording may cause accidental use from generic design requests.

Mitigation: Invoke Lovart explicitly for Lovart.ai work and review generated API calls before execution.

Risk: Lovart API keys can be exposed if copied into client-side code or shared logs.

Mitigation: Store LOVART_API_KEY in an environment variable or server-side secret store, proxy requests through approved backend services, and rotate keys regularly.

## Reference(s):

- [Lovart API Documentation](https://lovart.info/lovart-api)
- [Lovart for Developers](https://lovart.info/lovart-ai-code)
- [Lovart.ai](https://www.lovart.ai/)
- [ClawHub Skill Page](https://clawhub.ai/mendynew/skills/lovart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optimized design prompts, Lovart.ai API request examples, polling commands, result handling guidance, and configuration instructions for LOVART_API_KEY.]

## Skill Version(s):

1.0.0 (source: release evidence, skill frontmatter, config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
