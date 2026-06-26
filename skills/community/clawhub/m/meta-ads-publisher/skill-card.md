## Description: <br>
Executes Meta Ads campaign management tasks, including creating campaigns, changing budgets, pausing or activating entities, duplicating campaigns, and summarizing results with a required Meta access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, growth teams, and developers use this skill to guide an agent through Meta Ads campaign creation, updates, duplication, reporting, and activation review. It is intended for accounts where the user has authorized Meta Marketing API access and can confirm budgets, targeting, creative, and status changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make write operations against a Meta Ads account, including campaign creation, budget changes, duplication, and activation. <br>
Mitigation: Use a revocable least-privilege Meta access token, confirm the exact ad account and object IDs, and require user confirmation for campaign, ad set, ad, budget, and status changes. <br>
Risk: Advertising spend can be affected if a new, duplicated, or modified campaign is activated before review. <br>
Mitigation: Create or duplicate campaigns in PAUSED status, keep them paused until Ads Manager review is complete, and confirm budget and targeting before activation. <br>
Risk: The required Meta access token and ad account ID are sensitive credentials. <br>
Mitigation: Store credentials only in secret management, never print tokens in plain text, and use the token only for the Meta Marketing API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/meta-ads-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/elias-didoo) <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [Meta Graph API v21.0 Endpoint](https://graph.facebook.com/v21.0/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown with curl command examples, checklists, summaries, and readable tables for campaign lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; campaign and ad changes should be summarized after execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
