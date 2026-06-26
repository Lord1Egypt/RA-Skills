## Description: <br>
导购专家，回答用户购物相关问题，并给购买链接；当用户咨询购物问题、价格或优惠活动时，支持通过关键词或京东、淘宝、天猫商品链接搜索价格、优惠券和购买链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachariah-77](https://clawhub.ai/user/zachariah-77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shopping users and agents use this skill to search Mainland China e-commerce listings, compare prices, find coupons, and return purchase links for product keywords or submitted item URLs. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Shopping keywords, product URLs, and the optional LINKBOT_API_KEY are sent to linkbot-api.linkstars.com. <br>
Mitigation: Install only when sending that shopping data to the external service is acceptable, and use a dedicated LINKBOT_API_KEY for commission attribution. <br>
Risk: Without a valid LINKBOT_API_KEY, the service may use a default configuration rather than attributing commissions to the user. <br>
Mitigation: Configure LINKBOT_API_KEY from the provider before use when commission attribution matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zachariah-77/linkbot) <br>
- [Haohuo Service Homepage](https://www.haohuo.com) <br>
- [Linkbot API Endpoint](https://linkbot-api.linkstars.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with product summaries, prices, coupon details, and purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are formatted from an external API response; each platform parser returns up to five items.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
