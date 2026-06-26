## Description: <br>
[Didoo AI] Analyzes Meta Ads campaign performance in depth, including metrics, funnel health, trends, and anomalies, and outputs structured analysis without recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, growth teams, and agents use this skill to analyze Meta Ads campaign performance for a selected account, campaign level, time range, and attribution window. It helps identify funnel weak points, metric trends, anomalies, and data quality caveats before any separate recommendation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth credentials and an ad account identifier that let the agent read Meta Ads account data. <br>
Mitigation: Use a least-privilege ads_read token, provide only the intended ad account ID, and revoke or rotate the token when the analysis is complete. <br>
Risk: Broad trigger phrases such as analyze, diagnose, or full audit could activate the skill when the user intended another analytics domain. <br>
Mitigation: Confirm the user means Meta Ads and verify the account, campaign, date range, and attribution window before making API calls. <br>
Risk: Campaign metrics can be unstable for short time ranges, low impression counts, or recently edited campaigns. <br>
Mitigation: Call out data-quality limits in the output and avoid strong conclusions when the artifact's stated thresholds are not met. <br>


## Reference(s): <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [ClawHub skill page](https://clawhub.ai/elias-didoo/meta-ads-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/elias-didoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Structured Markdown analysis with campaign context, summary metrics, funnel analysis, trend analysis, key issues, and data notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Meta Ads data through required META_ACCESS_TOKEN and META_AD_ACCOUNT_ID credentials; stores session context keys for downstream analysis and recommendation workflows.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
