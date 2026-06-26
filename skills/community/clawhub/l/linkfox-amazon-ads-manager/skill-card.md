## Description: <br>
Amazon Ads Manager helps agents query, create, and update Sponsored Products, Sponsored Brands, and Sponsored Display campaigns, ad groups, ads, targeting, budget rules, and related advertising entities through LinkFox-authenticated Amazon Ads workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, advertising operators, and agent developers use this skill to manage Amazon Ads entities across SP, SB, and SD accounts. It supports listing metadata and performing create or update actions for campaigns, ad groups, ads, targets, keywords, creatives, budget rules, bids, budgets, names, and statuses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create and update actions can make live Amazon Ads spend changes, including bid, budget, status, and budget-rule changes. <br>
Mitigation: Require explicit confirmation before create or update actions and review the target account, region, entity count, and each budget or bid change. <br>
Risk: The skill requires sensitive credentials and Amazon Ads authority through LinkFox. <br>
Mitigation: Install only for users who accept that authority, keep credentials scoped to the intended accounts, and avoid broad automatic instructions for spend-affecting changes. <br>


## Reference(s): <br>
- [Amazon Ads Manager ClawHub listing](https://clawhub.ai/linkfox-ai/linkfox-amazon-ads-manager) <br>
- [Parameter and Field Reference Overview](references/api.md) <br>
- [Sponsored Products API Reference](references/api/sp.md) <br>
- [Sponsored Brands API Reference](references/api/sb.md) <br>
- [Sponsored Display API Reference](references/api/sd.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, guidance] <br>
**Output Format:** [JSON API responses with concise Markdown confirmations, error guidance, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox API credentials and Amazon Ads authorization; create and update actions can affect live advertising spend.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
