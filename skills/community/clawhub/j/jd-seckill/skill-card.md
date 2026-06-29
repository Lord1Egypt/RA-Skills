## Description: <br>
Queries JD.com flash-sale products and returns filtered product recommendations with prices, quality signals, image URLs, and purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping-assistant agents use this skill to browse JD.com flash-sale items, narrow results by category keyword or price, and compare recommendations before opening purchase links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries are sent through the publisher's Tencent Cloud proxy before reaching JD.com. <br>
Mitigation: Install only if that data flow is acceptable, avoid entering sensitive personal information in queries, and review network behavior before use. <br>
Risk: Purchase links may be routed through JD Union-style affiliate or link-generation infrastructure. <br>
Mitigation: Verify the final destination, seller, price, and terms directly on JD.com before buying. <br>
Risk: The listing emphasizes JD self-operated products, while the security evidence notes backend support for flagship-store items and broader affiliate/search endpoints. <br>
Mitigation: Treat self-operated-only claims cautiously and inspect returned shop metadata, especially the shop name and self-operated flag, before relying on recommendations. <br>
Risk: The artifact includes a shared cloud proxy token. <br>
Mitigation: Treat the proxy token as non-secret client material, monitor for misuse, and rotate or restrict proxy credentials server-side where possible. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cn-shopping/jd-seckill) <br>
- [Publisher profile](https://clawhub.ai/user/cn-shopping) <br>
- [JD Open API router endpoint](https://api.jd.com/routerjson) <br>
- [Configured Tencent Cloud proxy endpoint](https://1439498936-23pvh3iikx.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON string containing a summary and product-list data; agents may render product images and purchase links as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paginated product recommendations with item names, prices, discount estimates, shop metadata, quality signals, image URLs, and purchase URLs.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
