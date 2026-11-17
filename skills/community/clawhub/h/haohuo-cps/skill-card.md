## Description:

电商 CPS 助手，面向 CPS 推广者的电商选品与转链工具，支持商品链接转链、淘口令/短链解析、佣金率查询、关键词选品比价，目前支持京东/淘宝/天猫平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachariah-77](https://clawhub.ai/user/zachariah-77)

### License/Terms of Use:

MIT-0

## Use Case:

External affiliate and CPS promoters use this skill to search products, compare prices and coupons, convert JD/Taobao/Tmall links or Taobao tokens into promotional links, and review commission rates.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Shopping queries, product links, Taobao tokens, and LINKBOT_API_KEY are sent to the provider service.

Mitigation: Install only when affiliate/CPS shopping lookup is intended, and avoid submitting sensitive product links or tokens.

Risk: Promotional links and commission rates are commercial affiliate output and may not be neutral product advice.

Mitigation: Present affiliate links and commission rates clearly so users can evaluate recommendations with that commercial context.

Risk: Without a valid LINKBOT_API_KEY, commission attribution may use the service default rather than the user's account.

Mitigation: Configure LINKBOT_API_KEY before deployment when user-attributed commissions are required, and show the no-key notice when it appears in tool output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachariah-77/skills/haohuo-cps)
- [Publisher profile](https://clawhub.ai/user/zachariah-77)
- [星罗好货](https://www.haohuo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with product details, prices, coupon notes, commission rates, and promotional links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and LINKBOT_API_KEY for user-attributed commissions; without a valid key the service may use default attribution.]

## Skill Version(s):

1.0.7 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
