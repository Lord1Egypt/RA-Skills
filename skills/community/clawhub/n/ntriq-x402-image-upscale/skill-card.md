## Description:

AI image upscaling using Real-ESRGAN. 2x/3x/4x super-resolution for photos and general images. $0.10 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to submit jpg, png, or webp images to a paid remote image-upscaling service and receive 2x, 3x, or 4x super-resolution output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images or image URLs are processed by the provider's remote service and may reveal image contents or metadata.

Mitigation: Avoid sensitive, private, regulated, or confidential images unless the provider's privacy and retention practices are acceptable.

Risk: Each successful call is documented as costing $0.10 USDC.

Mitigation: Confirm the intended image, scale, and payment header before sending the request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-image-upscale)
- [Publisher profile](https://clawhub.ai/user/ntriq-gh)
- [Provider homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with bash and JSON examples; service responses are JSON containing base64-encoded PNG image data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an x402 payment header and sends image URLs or base64 image data to a remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
