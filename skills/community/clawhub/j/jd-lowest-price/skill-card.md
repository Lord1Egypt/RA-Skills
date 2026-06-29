## Description: <br>
提供京东历史最低价商品查询，按关键词、价格、好评率、销量和排序条件返回精选商品信息、图片和购买链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
购物用户和代理可用该技能发现京东历史最低价商品，按品类关键词、预算、好评率和排序方式筛选候选商品。代理可将返回的商品名称、价格、图片、店铺、销量、好评率和购买链接整理成面向用户的推荐结果。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping search parameters are sent to the publisher's Tencent cloud proxy and JD APIs. <br>
Mitigation: Use the skill only for shopping searches the user is comfortable sending to those services. <br>
Risk: The security guidance notes that artifacts allow flagship-store results despite stricter self-operated wording. <br>
Mitigation: Verify store type, final price, and purchase link before relying on a recommendation or buying. <br>
Risk: Lowest-price product availability and prices can change quickly. <br>
Mitigation: Treat results as discovery leads and confirm current price and stock at checkout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/jd-lowest-price) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON product data with a short natural-language summary; agents may render product images and purchase links in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inputs include optional keyword, maximum price, sort order, minimum good-comment rate, and page number.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
