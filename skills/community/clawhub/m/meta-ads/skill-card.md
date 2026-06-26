## Description: <br>
Manage Meta Ads campaigns, ad sets, ads, creatives, and performance metrics through the Meta Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachgodsell93](https://clawhub.ai/user/zachgodsell93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing operators and developers use this skill to let an agent inspect and manage Meta ad accounts, campaigns, ad sets, ads, creatives, budgets, statuses, and reporting metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to activate, delete, create, update, or change budgets for real Meta Ads campaigns. <br>
Mitigation: Use a dedicated least-privilege token scoped to the intended ad account, set spend limits in Meta Business Manager, and require explicit approval before activation, budget changes, creation, update, or delete actions. <br>
Risk: A broad or mishandled Meta access token could expose live advertising account control. <br>
Mitigation: Store META_ACCESS_TOKEN outside the skill content, rotate it as needed, and prefer a dedicated token with only ads_read and ads_management for the intended account. <br>


## Reference(s): <br>
- [Meta Graph API v25.0](https://graph.facebook.com/v25.0/) <br>
- [ClawHub package page](https://clawhub.ai/zachgodsell93/meta-ads) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; examples can create, update, activate, pause, or delete live ads resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
