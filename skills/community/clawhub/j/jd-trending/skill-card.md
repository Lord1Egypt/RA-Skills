## Description: <br>
提供实时热销频道商品查询工具，展示当前畅销好货，仅筛选京东自营商品，已精选好评≥98%、销量≥2000的品质商品，支持按品类关键词、价格筛选和多种排序，结果不足时自动降级保证推荐数量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
消费者和购物助手代理使用该技能查询京东自营实时热销商品，并按关键词、最高价格、好评率、排序方式和页码筛选商品推荐。该技能返回商品列表和摘要提示，供代理展示商品图片、价格、优惠后价格、分类、销量、好评率和购买链接。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches are routed through a third-party cloud proxy with an embedded token. <br>
Mitigation: Review proxy transparency and token handling before installation, and avoid using the skill where self-operated-only shopping data paths are required. <br>
Risk: Included proxy code supports broader JD affiliate/proxy operations than the advertised trending-products tool. <br>
Mitigation: Review the shipped artifact behavior against the intended deployment scope and monitor outbound requests to confirm only expected read-only shopping queries are used. <br>
Risk: The skill provides product information and purchase links but does not control inventory, price changes, or final purchase decisions. <br>
Mitigation: Have the agent present results as current recommendations for user review and require users to verify price, stock, merchant, and purchase details on JD before buying. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cn-shopping/jd-trending) <br>
- [JD Open API endpoint](https://api.jd.com/routerjson) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, guidance] <br>
**Output Format:** [JSON string containing content and summary fields; content is a JSON-formatted product list intended for markdown rendering.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product image URLs, buy URLs, prices, discount percentages, category names, recent order counts, good-comment rates, and pagination guidance.] <br>

## Skill Version(s): <br>
0.3.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
