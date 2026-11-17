## Description:

Create handheld product short videos via Infinimo AI Design with avatar first-frame compositing, AI script writing, image-to-video submission, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce operators use this skill to create avatar-led product demo videos, shoppable shorts, and listing promo videos from product images, prompts, and selected Infinimo model settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, product images or image URLs, and token-authenticated requests are sent to the clawec.com/Infinimo service.

Mitigation: Use the skill only for assets intended for that service, avoid sensitive product material unless upload is intended, and manage Infinimo API tokens through environment variables.

Risk: The documented delete endpoint may remove video log history.

Mitigation: Confirm the target log entry before using deletion behavior and preserve any needed video URLs or audit details first.

## Reference(s):

- [Handheld Product Video Response Schema](references/response-schema.md)
- [Infinimo AI Design](https://design.infinimo.ai/?source=q-i-d-clawhub)
- [Infinimo API Key](https://design.infinimo.ai/api-key?source=q-i-d-clawhub)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/infinimo-ai-design-product-video-create)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with bash command examples and JSON response references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include selected avatar, first-frame URL, submitted video URL, and parameter summaries from Infinimo API responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
