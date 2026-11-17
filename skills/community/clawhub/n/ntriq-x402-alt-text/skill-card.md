## Description:

Generate WCAG-compliant alt text and detailed image descriptions for accessibility. Pay $0.01 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to generate concise alt text and more detailed accessibility descriptions for images in libraries, CMS workflows, or e-commerce catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or image URLs are sent to ntriq's external service.

Mitigation: Use only images approved for external processing, and avoid private or sensitive images unless the provider's privacy and retention terms are acceptable.

Risk: Each API call requires a paid x402 transaction.

Mitigation: Verify the x402 payment flow and confirm the disclosed $0.01 USDC per-call cost before installation or automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-alt-text)
- [ntriq X402 homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON response containing alt_text and description fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alt text is intended to be concise, with optional language selection when calling the service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
