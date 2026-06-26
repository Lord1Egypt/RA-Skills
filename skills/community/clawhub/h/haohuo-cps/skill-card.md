## Description: <br>
电商 CPS 助手，面向 CPS 推广者的电商选品与转链工具，支持商品链接转链、淘口令/短链解析、佣金率查询、关键词选品比价，目前支持京东、淘宝和天猫平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachariah-77](https://clawhub.ai/user/zachariah-77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External CPS affiliate marketers and shopping-assistant agents use this skill to search JD, Taobao, and Tmall products, resolve product links or Taobao tokens, compare prices and coupons, and return affiliate links with commission rates. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Searches, product links, Taobao tokens, and LINKBOT_API_KEY are sent to the declared Linkbot API service. <br>
Mitigation: Use only with data appropriate for this shopping affiliate workflow and configure a provider-issued LINKBOT_API_KEY when account attribution matters. <br>
Risk: If LINKBOT_API_KEY is missing or invalid, generated affiliate commissions may not be attributed to the user's account. <br>
Mitigation: Set LINKBOT_API_KEY before use and show any no-key warning returned by the script to the user. <br>
Risk: Responses include promotion links and commission rates that can affect shopping and affiliate decisions. <br>
Mitigation: Present product information, promotion links, and commission rates together so users can evaluate the commercial context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zachariah-77/haohuo-cps) <br>
- [星罗好货 homepage](https://www.haohuo.com) <br>
- [Linkbot API service endpoint](https://linkbot-api.linkstars.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown product results with prices, coupons, commission rates, affiliate links, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, network access, and LINKBOT_API_KEY for user-attributed commissions; sends searches, product links, Taobao tokens, and the API key to linkbot-api.linkstars.com.] <br>

## Skill Version(s): <br>
1.0.7 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
