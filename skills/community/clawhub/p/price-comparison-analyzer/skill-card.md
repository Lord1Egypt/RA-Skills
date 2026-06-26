## Description: <br>
对多平台商品价格进行聚合分析与风险评估，输出可行动的购买建议，避免伪低价与条件陷阱误导 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long1973m](https://clawhub.ai/user/long1973m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to compare public e-commerce prices for a clearly defined product, evaluate channel and condition risks, and produce actionable purchase recommendations. It is intended for advisory price comparison, not for payment, account access, or seller dispute resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations can be misleading when public price data is stale, incomplete, or not aligned to the same SKU. <br>
Mitigation: Confirm the product configuration, region, platform list, source links, and collection time before acting on a recommendation. <br>
Risk: Risk labels are advisory, and the security evidence notes that the current script may misclassify some recommendations. <br>
Mitigation: Double-check unusually low prices and high-impact purchase decisions against official platform terms, seller status, warranty coverage, and return policy. <br>
Risk: Users may over-share private shopping or account information while requesting price comparisons. <br>
Mitigation: Do not provide account credentials, payment information, order histories, cookies, or other private shopping data. <br>


## Reference(s): <br>
- [电商比价输入数据格式规范](artifact/references/input_format.md) <br>
- [电商价格采集指导](artifact/references/price_collection_guide.md) <br>
- [电商比价风险评估规则](artifact/references/risk_assessment_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Structured JSON recommendations by default, with optional natural-language risk explanations and internal analysis evidence when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output separates user-facing recommendations from deeper risk explanations and internal model evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
