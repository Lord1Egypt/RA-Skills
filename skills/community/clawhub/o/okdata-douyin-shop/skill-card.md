## Description:

Provides public Douyin Shop product, review, and store data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve public Douyin Shop affiliate product listings, product details and reviews, and store product listings for research and comparison. Paid calls cost $0.039–$0.054 each.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and item identifiers are sent to the external okdata API.

Mitigation: Review inputs before calling and avoid sending sensitive information; use the API only if you trust the provider.

Risk: API calls are paid, and additional result pages require additional calls.

Mitigation: Check the per-call price and cap each call with max_price; request more pages only when needed.

## Reference(s):

- [Douyin Shop API reference](https://okdata.online/apis/douyin_shop/?src=skill-okdata-douyin-shop)
- [okdata agent setup guide](https://okdata.online/agents.md)
- [ClawHub release page](https://clawhub.ai/conn-ho/skills/okdata-douyin-shop)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text data returned from okdata API calls, with source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require separate paid calls.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
