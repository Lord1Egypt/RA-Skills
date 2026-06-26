## Description: <br>
x402 pay-per-call API for Amazon product search, filtering, ranking, detailed extraction, and one-shot best-products recommendations, with no API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hashcatter](https://clawhub.ai/user/hashcatter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, filter, rank, and inspect Amazon products through the HashCats API. It is suited for shopping research and product-intelligence workflows where structured JSON results and x402 micropayments are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger small USDC payments through x402 when the agent calls HashCats endpoints. <br>
Mitigation: Use wallet spending limits, monitor first use, and avoid unattended repeated calls unless cumulative charges are acceptable. <br>
Risk: Shopping queries and Amazon product URLs are sent to HashCats for processing. <br>
Mitigation: Avoid sending sensitive or private shopping intent unless sharing that data with HashCats is acceptable. <br>


## Reference(s): <br>
- [HashCats API homepage](https://api.hashcats.io) <br>
- [HashCats API docs](https://api.hashcats.io/docs) <br>
- [HashCats OpenAPI schema](https://api.hashcats.io/openapi.json) <br>
- [ClawHub skill page](https://clawhub.ai/hashcatter/hashcats-amazon) <br>
- [HashCatter publisher profile](https://clawhub.ai/user/hashcatter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON] <br>
**Output Format:** [Markdown instructions for the agent, with API responses returned as structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require x402 wallet payment before API responses are returned.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, changelog released 2026-04-18, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
