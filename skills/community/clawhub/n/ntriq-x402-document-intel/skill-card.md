## Description:

Extract text, classify document type, and pull tables from any document image. Pay $0.05 USDC per call via x402 (no API key needed).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call a paid document-intelligence API for text extraction, summarization, classification, and table extraction from document images supplied by public URL or base64.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document images or URLs are sent to the operator of x402.ntriq.co.kr despite local/no-cloud wording in the artifact.

Mitigation: Do not use confidential, regulated, or personal documents unless the operator's privacy, retention, deletion, and payment terms are acceptable.

Risk: x402 payment signing can authorize a USDC payment on Base mainnet.

Mitigation: Verify the wallet, network, amount, recipient, nonce, and expiration before signing any payment payload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-document-intel)
- [ntriq homepage](https://x402.ntriq.co.kr)
- [Document Intel API endpoint](https://x402.ntriq.co.kr/document-intel)
- [Service catalog](https://x402.ntriq.co.kr/services)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public image URL or base64 document image, an analysis type, and an x402 payment header for paid calls.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
