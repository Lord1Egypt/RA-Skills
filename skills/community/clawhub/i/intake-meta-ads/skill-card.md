## Description: <br>
Intake Breathing META ads analyst for Meta/Facebook/Instagram ad performance, Marketing API data pulls, campaign diagnostics, creative analysis, budget reallocation, pixel/tracking audits, and offer-level performance forensics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxwaggoner](https://clawhub.ai/user/maxwaggoner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External media buyers and marketing operators use this skill to pull Intake Breathing Meta ads data, diagnose CPA and ROAS issues, evaluate creative and campaign efficiency, and prepare prioritized optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized account access or overbroad credential use could expose Meta ads data. <br>
Mitigation: Use the skill only with authorization for the Intake Breathing ad account and provide a fresh short-lived token limited to ads_read. <br>
Risk: Access tokens may be exposed if pasted into retained transcripts or shared logs. <br>
Mitigation: Use secure secret input when available and avoid storing tokens in prompts, files, or command history. <br>
Risk: CSV or JSON exports can contain sensitive campaign performance data. <br>
Mitigation: Store exports only in approved locations and delete or protect them after analysis. <br>


## Reference(s): <br>
- [Intake Breathing META Account Context](references/intake-account-context.md) <br>
- [Intake Breathing Diagnostic Playbooks](references/intake-diagnostics.md) <br>
- [Campaign Insights API Reference](references/campaign-insights-api.md) <br>
- [Meta Marketing API Insights](https://developers.facebook.com/docs/marketing-api/insights) <br>
- [Meta Ad Account Insights Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown analysis with shell commands and CSV or JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Meta ads_read access token to query the Marketing API and can save campaign, ad, trend, ROAS, and demographic exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, frontmatter, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
