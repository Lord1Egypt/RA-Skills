## Description:

Provides a unified JisuAPI gateway for agents to call supported data APIs such as weather, gold prices, stocks, delivery tracking, exchange rates, OCR, and vehicle data through one configured API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a structured data gateway when they need one configured JisuAPI key to query multiple categories of JisuAPI data. Typical requests include weather, market prices, exchange rates, delivery tracking, QR or barcode handling, OCR, and vehicle information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit user-provided phone numbers, ID card numbers, bank card numbers, IPs, addresses, VINs, QR or barcode content, and OCR image data to JisuAPI.

Mitigation: Use it only when third-party data sharing is acceptable, obtain appropriate user consent, and avoid sending sensitive documents or financial identifiers unless there is a clear need.

## Reference(s):

- [JisuAPI documentation](https://www.jisuapi.com/)
- [JisuAPI base API endpoint](https://api.jisuapi.com)
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [JSON API responses with Markdown command examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; API access, quota, and billing depend on the user's JisuAPI account.]

## Skill Version(s):

1.0.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
