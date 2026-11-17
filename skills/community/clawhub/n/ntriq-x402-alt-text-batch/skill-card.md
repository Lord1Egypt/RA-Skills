## Description:

Batch-generate WCAG-compliant alt text for up to 500 images in one call. Flat $3.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to call a paid remote service that generates WCAG-oriented alt text and image descriptions for batches of image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted image URLs and shared context are data shared with the ntriq service operator.

Mitigation: Do not submit private, internal-only, authenticated, or confidential images or context unless provider access, retention, and logging practices have been independently verified.

Risk: The skill requires payment through x402 for normal use.

Mitigation: Install and use it only when the agent operator is comfortable paying the listed $3.00 USDC charge and handling the required x402 payment header.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-alt-text-batch)
- [ntriq service homepage](https://x402.ntriq.co.kr)
- [Alt text batch API endpoint](https://x402.ntriq.co.kr/alt-text-batch)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown instructions with HTTP/curl examples and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch size up to 500 image URLs; optional shared context, max_length, and language parameters; paid $3.00 USDC x402 call.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
