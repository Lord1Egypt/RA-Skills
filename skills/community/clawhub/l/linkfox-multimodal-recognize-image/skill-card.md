## Description:

Analyzes publicly accessible image URLs with LinkFox's multimodal image-recognition API to return text descriptions, OCR-style extraction, visual Q&A, and product-image analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route image-description, OCR extraction, visual question answering, and e-commerce product-image review tasks to LinkFox. It can convert local image files into temporary public URLs before analysis when the user accepts that upload behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image recognition and local-image upload use a paid external LinkFox service and may consume compute credits.

Mitigation: Tell users before additional calls may incur cost, reuse the built-in 24-hour cache where appropriate, and avoid repeated retries without user consent.

Risk: Local image uploads are converted into publicly reachable URLs for analysis.

Mitigation: Avoid private or sensitive local images unless the user explicitly accepts public upload exposure and the temporary URL behavior.

Risk: The skill performs authentication, API-key creation, billing-plan listing, payment-order creation, and feedback reporting.

Mitigation: Use only official LinkFox endpoints, verify environment variables before use, avoid casually sharing SMS codes or API keys, and prefer safer secret storage over shell startup files.

Risk: Endpoint environment variables can redirect requests away from the default LinkFox hosts.

Mitigation: Confirm configured LinkFox endpoint variables point to expected official hosts before sending credentials, images, or billing requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-multimodal-recognize-image)
- [Image Recognition API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses containing text analysis and cost fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recognition script stores full JSON responses in a local LinkFox session directory, prints small responses inline, summarizes larger responses unless --inline is used, and caches identical calls for 24 hours.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
