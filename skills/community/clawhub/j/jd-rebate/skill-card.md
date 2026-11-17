## Description:

京东返利帮助用户完成返利授权、识别淘宝、京东、拼多多商品链接、搜索商品，并返回后续可生成返利链接的商品结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfile](https://clawhub.ai/user/skyfile)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find rebate-capable products, convert supported shopping links into rebate results, complete WeChat authorization, check rebate balances, and confirm withdrawal requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit withdrawal requests after chat confirmation.

Mitigation: Review withdrawal flows before installation and require users to confirm withdrawal amounts before submitting requests.

Risk: The skill stores WeChat identifiers locally and can generate links that include OpenID-bearing account details.

Mitigation: Install only in trusted workspaces and limit access to local skill data files and generated account-detail links.

Risk: The skill depends on a third-party rebate backend for authorization, balances, product search, link generation, and withdrawals.

Mitigation: Use only if the rebate backend is trusted and monitor failures or unexpected responses before relying on returned rebate information.

Risk: The skill may use a configured model API key during product-intent handling.

Mitigation: Use a restricted model API key for the workspace where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfile/skills/jd-rebate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown user messages with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product search results, rebate links, account balance details, and withdrawal confirmation messages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
