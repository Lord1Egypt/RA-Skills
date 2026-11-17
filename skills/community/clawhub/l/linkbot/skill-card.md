## Description:

A shopping assistant that answers product, price, coupon, and deal questions and returns purchase links for JD, Taobao, and Tmall using keyword or product-link queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachariah-77](https://clawhub.ai/user/zachariah-77)

### License/Terms of Use:

MIT-0

## Use Case:

External users in Mainland China use this skill to search products, compare prices, find coupons or subsidies, and convert product links into purchase links. It is intended for shopping recommendations and deal lookup across supported Chinese e-commerce platforms.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Shopping queries, product links, and the configured API key are sent to linkbot-api.linkstars.com.

Mitigation: Use only when the user is comfortable sending shopping data to the provider, and avoid submitting sensitive product links or private account information.

Risk: The skill returns affiliate purchase links that may influence buying decisions and commission attribution.

Mitigation: Disclose the affiliate-link behavior when relevant and encourage users to verify final price, coupon, and seller details before purchase.

Risk: The skill depends on the Python requests package installed through pip3.

Mitigation: Install in an isolated Python environment and review or pin the dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachariah-77/skills/linkbot)
- [Publisher profile](https://clawhub.ai/user/zachariah-77)
- [Service homepage](https://www.haohuo.com)
- [Linkbot API provider](https://linkbot-api.linkstars.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with product details, prices, coupon information, and purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, network access, the requests package, and optionally LINKBOT_API_KEY for user-attributed affiliate links.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
