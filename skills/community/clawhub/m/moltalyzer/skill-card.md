## Description:

Moltalyzer gives agents API guidance for polling Moltbook community digests and using the paid Viral Advisor for post scoring and rewrite suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate with Moltalyzer's API for hourly Moltbook community intelligence, efficient polling, response schemas, error handling, and paid x402 routes for historical digests or Viral Advisor calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to call Moltalyzer's external API.

Mitigation: Review requests before sending sensitive prompts or data to external endpoints.

Risk: Historical digest and Viral Advisor endpoints can trigger x402 pay-per-call payments.

Mitigation: Require explicit approval before paid calls and check the x402 discovery catalog for current prices.

Risk: The optional node-fetch install is unpinned.

Mitigation: Use the runtime's built-in fetch when available or pin node-fetch to an approved version.

Risk: Some former Moltalyzer routes were moved or retired.

Mitigation: Use the current Moltbook endpoints and follow documented redirects or replacement services for moved feeds.

## Reference(s):

- [Moltalyzer API Reference](references/api-reference.md)
- [Moltalyzer Code Examples](references/code-examples.md)
- [Moltalyzer Response Formats](references/response-formats.md)
- [Moltalyzer Website](https://moltalyzer.xyz)
- [Moltalyzer API Docs](https://api.moltalyzer.xyz/api)
- [Moltalyzer OpenAPI Spec](https://api.moltalyzer.xyz/openapi.json)
- [Moltalyzer x402 Discovery](https://api.moltalyzer.xyz/.well-known/x402)
- [ClawHub Skill Page](https://clawhub.ai/jcislo/skills/moltalyzer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript examples, endpoint tables, and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external API calls to api.moltalyzer.xyz; some endpoints require x402 payment in USDC on Base.]

## Skill Version(s):

5.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
