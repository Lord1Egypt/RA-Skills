## Description:

搜索美团全国连锁品牌酒店特价套餐，支持按城市和品牌筛选、按折扣或价格排序，并返回价格、有效期、评分和美团预订链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to find discounted chain-hotel packages in Chinese domestic cities, compare price and discount details, and open Meituan booking links.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Hotel search terms are sent through the publisher's Tencent Cloud proxy.

Mitigation: Install only when this proxy use is acceptable, and avoid sending sensitive or unnecessary travel details.

Risk: Prices, availability, and booking terms may change after the skill returns results.

Mitigation: Confirm price, inventory, validity period, and booking terms on Meituan before purchase.

Risk: Broad hotel-search trigger wording may cause the skill to respond to ambiguous travel requests.

Mitigation: Review ambiguous requests before relying on the returned hotel recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/meituan-hotel-deals)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown-formatted hotel search results with image URLs, pricing details, validity dates, ratings, and booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 hotel packages per query; prices and inventory can change and should be confirmed on Meituan before booking.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
