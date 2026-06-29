## Description: <br>
提供9.9包邮频道商品查询工具，展示超值低价好货，仅筛选京东自营商品，已精选好评≥98%、销量≥2000的品质商品，支持按品类关键词、价格筛选和多种排序，结果不足时自动降级保证推荐数量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to browse JD 9.9包邮 product recommendations by category keyword, price ceiling, quality threshold, sort order, and page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports broader JD affiliate search and promotion-link capabilities than the public description discloses. <br>
Mitigation: Review before installing when strict JD self-operated-only filtering or tight affiliate API scope is required; validate proxy behavior and disclosed capabilities before use. <br>
Risk: Product recommendations, prices, availability, images, and purchase links depend on live JD data and may change. <br>
Mitigation: Treat results as shopping guidance only and verify price, seller, availability, and terms on JD before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/jd-99-baoyou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON string containing product records and a summary suitable for Markdown presentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paginated shopping results with product image URLs and purchase links; live results depend on JD API and proxy availability.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
