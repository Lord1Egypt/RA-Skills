## Description: <br>
Query, audit, and optimize Google Ads campaigns using Google Ads API access or browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and marketing operators use this skill to inspect Google Ads performance, identify wasted spend, audit conversion tracking, download reports, and prepare account optimization actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through high-impact Google Ads account changes such as pausing campaigns, pausing keywords, enabling items, or changing budgets. <br>
Mitigation: Require a clear preview of affected accounts, campaigns, keywords, budgets, and expected impact, then obtain explicit user confirmation before any account mutation. <br>
Risk: The skill uses Google Ads credentials and may inspect local configuration such as ~/.google-ads.yaml or GOOGLE_ADS_* environment variables. <br>
Mitigation: Avoid printing credential files or tokens, use the narrowest account access available, and handle OAuth, developer token, and customer ID values as sensitive data. <br>
Risk: Downloaded, exported, or emailed reports may contain sensitive business performance data. <br>
Mitigation: Treat exports as confidential business data and confirm destination, recipients, and storage location before downloading, sharing, or scheduling reports. <br>


## Reference(s): <br>
- [Google Ads ClawHub Skill Page](https://clawhub.ai/jdrhyne/google-ads) <br>
- [Google Ads API Setup](references/api-setup.md) <br>
- [Google Ads Browser Automation Workflows](references/browser-workflows.md) <br>
- [Google Ads Web UI](https://ads.google.com/aw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, inline code, shell commands, Python snippets, and recommended account actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Google Ads account data, downloaded reports, credential configuration, and proposed campaign or keyword changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
