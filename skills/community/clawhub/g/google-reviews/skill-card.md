## Description: <br>
Research Google Maps and Shopping reviews for any company. Run multi-brand monitoring with heartbeat refreshes and sentiment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators, analysts, and business teams use this skill to research company review signals across Google Business Profile, Google Shopping, and user-approved manual checks. It supports one-off reputation due diligence, competitor comparison, sentiment reporting, and optional recurring monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring monitoring can create local records of brand watchlists, normalized review snapshots, and reports. <br>
Mitigation: Review the planned contents of ~/google-reviews/ before enabling monitoring, and keep credentials, tokens, and private customer identifiers out of those files. <br>
Risk: Google API or manual review checks may send company, account, merchant, product, location, or query parameters to Google endpoints. <br>
Mitigation: Use user-approved access methods, scope Google account or API permissions narrowly, and prefer official APIs or user-provided exports when available. <br>
Risk: Automated alerts or outbound posting can create noise or unintended external communication. <br>
Mitigation: Keep alerts and outbound posting ask-first unless explicitly enabled, use cooldowns, and never claim live monitoring unless refresh jobs completed successfully. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/google-reviews) <br>
- [Skill homepage](https://clawic.com/skills/google-reviews) <br>
- [Setup](setup.md) <br>
- [Source Connectors](source-connectors.md) <br>
- [Review Schema](review-schema.md) <br>
- [Sentiment Rules](sentiment-rules.md) <br>
- [Heartbeat Recipes](heartbeat-recipes.md) <br>
- [Reporting Playbook](reporting-playbook.md) <br>
- [Google Business Profile API endpoint](https://mybusiness.googleapis.com) <br>
- [Google Merchant API endpoint](https://merchantapi.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, status digests, configuration notes, and optional shell snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use normalized JSONL review snapshots and local monitoring state under ~/google-reviews/ when recurring tracking is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
