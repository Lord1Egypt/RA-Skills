## Description:

Analyzes Intake Breathing Meta, Facebook, and Instagram ad performance, exports Marketing API insights, and guides campaign diagnostics, creative analysis, budget reallocation, tracking audits, and offer forensics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxwaggoner](https://clawhub.ai/user/maxwaggoner)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing operators and account analysts use this skill to pull Intake Breathing Meta Ads insights and turn campaign, ad, demographic, tracking, and offer data into concise performance findings and action recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks for a live Meta access token, and tokens may be exposed if pasted into normal chat or shell history.

Mitigation: Use a short-lived ads_read token, prefer a secret-entry mechanism when available, avoid logging token values, and revoke tokens after use.

Risk: Exported CSV or JSON reports can contain sensitive ad account performance data.

Mitigation: Store exports only in an approved secure location and remove local copies when the analysis is complete.

Risk: Budget and ROAS recommendations may be misleading while purchase value tracking is broken or incomplete.

Mitigation: Confirm purchase value and website_purchase_roas data before ROAS-based decisions, and treat CPA-only recommendations as provisional.

## Reference(s):

- [Intake META Ads Analyst on ClawHub](https://clawhub.ai/maxwaggoner/skills/intake-meta-ads)
- [Intake Breathing META Account Context](references/intake-account-context.md)
- [Intake Breathing Diagnostic Playbooks](references/intake-diagnostics.md)
- [Campaign Insights API Reference](references/campaign-insights-api.md)
- [Meta Marketing API Insights](https://developers.facebook.com/docs/marketing-api/insights)
- [Meta Ad Account Insights Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown analysis with tables, inline shell commands, and optional CSV or JSON export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a short-lived Meta ads_read access token and writes local campaign insight exports when API pulls are requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
