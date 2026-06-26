## Description: <br>
Helps hotel procurement teams compare real-time agricultural wholesale and ecommerce prices, then summarize price ranges and purchasing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hotel purchasing staff use this skill to check price ranges for food ingredients and ecommerce goods across public sources, with source and time labels for procurement decisions. It also supports approximate cost-floor analysis when users ask for cost breakdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names, supplier context, or purchasing intent may be sent to external search services during price lookup. <br>
Mitigation: Avoid confidential supplier plans, internal product names, sensitive cost details, and other private procurement data in prompts. <br>
Risk: Public web prices can be stale, region-specific, incomplete, or affected by logistics, seasonality, product grade, and minimum order quantities. <br>
Mitigation: Treat results as procurement references, verify against local suppliers before ordering, and preserve source and query-time labels in reports. <br>
Risk: Broad activation phrases such as price queries could trigger the skill unintentionally. <br>
Mitigation: Use explicit procurement-specific prompts and confirm the product, region, category, and intended analysis before acting on results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaoliuzhu/hotel-procurement-price-check) <br>
- [Ministry of Agriculture and Rural Affairs price monitoring](http://www.scs.moa.gov.cn/jcyj/) <br>
- [Agricultural market dynamics](http://www.agri.cn/sj/jcyj/) <br>
- [Yimutian wholesale platform](https://www.ymt.com/) <br>
- [Huinong market prices](https://www.cnhnb.com/pi/list) <br>
- [China Vegetable Network](http://www.vegnet.com.cn/) <br>
- [Beijing Xinfadi wholesale market](https://www.xinfadi.com.cn/) <br>
- [1688 Open Platform](https://open.1688.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown price reports with source and query-time annotations, plus optional bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price ranges, procurement suggestions, data-source caveats, and approximate cost-floor estimates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, released 2026-04-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
