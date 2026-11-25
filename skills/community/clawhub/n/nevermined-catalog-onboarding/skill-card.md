## Description:

Guides developers through validating an external x402 service, publishing and promoting it in the Nevermined Agent Services Catalog, and verifying a paid request through the Nevermined Router.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevermined-io](https://clawhub.ai/user/nevermined-io)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers use this skill to assess whether an external x402 service can be routed, validate its payment flow, and onboard, publish, and test its catalog listing. It also explains how operators can claim curated listings and when services can be paid for with Nevermined credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment helper and some referenced material were not fully assessed by the scanner.

Mitigation: Review the skill and payment helper before use, and test payment flows in the sandbox with a capped, disposable wallet.

Risk: Direct validation sends requests to a third-party merchant and can spend real funds; the helper uses a wallet private key.

Mitigation: Use synthetic test input, keep private keys out of conversations, and use only a throwaway wallet funded within a strict cap.

## Reference(s):

- [Nevermined Catalog documentation](https://nevermined.ai/docs/products/catalog/overview)
- [Nevermined Catalog Onboarding on ClawHub](https://clawhub.ai/nevermined-io/skills/nevermined-catalog-onboarding)
- [Direct-wallet validation](references/direct-wallet-pay.md)
- [Listing and promotion](references/list-and-promote.md)
- [Claiming listings and credits](references/claim-and-credits.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Code, Configuration instructions]

**Output Format:** [Markdown with shell, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
