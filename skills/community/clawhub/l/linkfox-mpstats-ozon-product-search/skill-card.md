## Description:

Searches MPSTATS data for Ozon Russia products by Russian keyword or SKU and returns product identity details such as product ID, title, brand, seller, page URL, and image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce analysts, sellers, and agents use this skill to find or reverse-lookup Ozon Russia products before choosing product, brand, seller, or detail workflows for deeper analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can collect phone and SMS login information, generate and persist API keys, and create billing or payment orders.

Mitigation: Use only trusted LinkFox credentials, avoid storing secrets in shared shell profiles, and run onboarding or billing flows only when the user intentionally requests those account actions.

Risk: The security evidence says the skill can write response and QR data to disk and send feedback externally.

Mitigation: Review local output paths before sharing workspaces and confirm external feedback reporting is acceptable for the use case.

Risk: The security evidence warns that environment variables can redirect LinkFox hosts.

Mitigation: Verify LinkFox environment variables point to official HTTPS LinkFox hosts before using the skill.

## Reference(s):

- [MPSTATS Ozon Product Search Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-mpstats-ozon-product-search)
- [MPSTATS Ozon 商品搜索 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands plus JSON API responses or saved JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The product search flow can write full responses to a local linkfox session directory, use a 24-hour local cache, and summarize large responses in stdout.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
