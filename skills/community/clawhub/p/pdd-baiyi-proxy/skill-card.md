## Description: <br>
Provides a Pinduoduo Baiyi subsidy shopping recommendation tool that searches a curated set of products by keyword, price range, brand-store status, sorting mode, and page, then returns product information with image URLs and purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse and filter Pinduoduo Baiyi subsidy product recommendations, compare prices and sales signals, and open purchase links for selected items. Agents can use it to answer shopping discovery requests with concise product summaries, image URLs, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries are sent to a third-party cloud proxy, and purchase links may be affiliate or commission tracked. <br>
Mitigation: Install only when users accept that data flow and monetization model; the publisher should clearly disclose affiliate tracking before routine use. <br>
Risk: Security evidence reports hardcoded commercial API credentials and an extra proxy stats/debug surface. <br>
Mitigation: The publisher should remove or rotate embedded credentials and document or disable the stats/debug surface before the skill is treated as routine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/pdd-baiyi-proxy) <br>
- [Publisher profile](https://clawhub.ai/user/cn-shopping) <br>
- [Cloud proxy endpoint](https://1439498936-44g9han8pj.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON content plus Markdown-ready shopping summaries with product image URLs and purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports keyword/category search, price bounds, brand-only filtering, sort selection, and pagination; product data may change as the proxy cache refreshes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
