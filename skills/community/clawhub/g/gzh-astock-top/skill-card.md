## Description: <br>
Retrieves A-share WeChat official account rankings, account metrics, latest article data, and subscription updates for a requested date using RedFox data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, content operators, financial professionals, and data analysts use this skill to monitor top A-share WeChat public accounts, compare engagement metrics, inspect recent article activity, and track subscribed accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured RedFox API key and requested account, date, or subscription queries to redfox.hk. <br>
Mitigation: Use the skill only when this external API use is acceptable, scope and rotate the key appropriately, and avoid exposing the key in prompts, logs, or shared files. <br>
Risk: Bundled subscription data and subscription commands can read or change local subscription state. <br>
Mitigation: Review or empty subscriptions.json before use and confirm add, remove, or clear actions before running subscription management commands. <br>
Risk: Engagement and article data reflect RedFox ingestion timing rather than live market or account state. <br>
Mitigation: Present results as indexed snapshot data and prefer queries after the documented daily update window. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/gzh-astock-top) <br>
- [Publisher Profile](https://clawhub.ai/user/redfox-data) <br>
- [RedFox API Guide](artifact/references/api_guide.md) <br>
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown tables and concise text generated from JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key; subscription workflows may update local JSON subscription state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
