## Description:

Query Maestro APIs over HTTP using the SIWX + JWT + x402 credit purchase flow. Resolve the exact endpoint from docs.gomaestro.org before requesting or paying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vardominator](https://clawhub.ai/user/vardominator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make direct Maestro API requests, resolve endpoint details from Maestro documentation, authenticate with SIWX, and purchase x402 credits only when required by the live service response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet signing and paid credit purchases for Maestro API calls.

Mitigation: Use a constrained wallet signer, fund it only with the intended spend, and require explicit approval for each payment recipient, token contract, network, and amount.

Risk: The skill may make additional credit purchases after initial confirmation if follow-up requests exhaust available credits.

Mitigation: Require explicit approval before every paid retry or additional credit purchase, and reuse the latest live 402 response for payment parameters.

## Reference(s):

- [SIWX + x402 Reference](references/siwx-x402.md)
- [Maestro documentation index](https://docs.gomaestro.org/llms.txt)
- [Maestro API Gateway](https://api.gomaestro.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP request details, response data, and concise next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected network, payment amount, signer address, credit headers, and settlement metadata when relevant.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
