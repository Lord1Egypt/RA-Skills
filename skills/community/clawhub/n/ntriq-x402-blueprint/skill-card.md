## Description:

AI architectural blueprint analysis - extract rooms, dimensions, materials from floor plans. $0.05 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to call a paid x402 blueprint-analysis service that extracts structured room, dimension, material, area, scale, and structural-element data from floor-plan images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blueprints and floor plans may contain sensitive building, occupancy, or security information and are sent to a remote API as either a URL or base64 image content.

Mitigation: Use only blueprint data you are authorized to submit, avoid restricted building plans, and review the provider's privacy and retention practices before use.

Risk: The service is paid per call through x402, so accidental or automated repeated requests may create unwanted charges.

Mitigation: Review generated API calls before execution and apply local rate limits, confirmation steps, or budget controls when integrating the skill into agent workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-blueprint)
- [Ntriq x402 Homepage](https://x402.ntriq.co.kr)
- [x402 Protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to submit either an image URL or base64 image content with an analysis type and optional language.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
