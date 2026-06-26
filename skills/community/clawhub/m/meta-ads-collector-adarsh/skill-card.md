## Description: <br>
Collects active Meta ads for a brand, reporting total ads, formats, ad types, longest-running ad duration, and estimated spend if available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing auditors and developers use this skill to gather public Meta Ad Library signals for a brand and feed paid ads metrics into a marketing audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a Meta access token for Ad Library API queries. <br>
Mitigation: Use a least-privilege Meta app token and keep secrets out of prompts, logs, and generated reports. <br>
Risk: The documented query defaults ad_reached_countries to US, which can make results unsuitable for audits needing broader geography. <br>
Mitigation: Confirm the required audit geography before relying on the output, and adjust country filters when broader coverage is needed. <br>


## Reference(s): <br>
- [Meta Ad Library API endpoint](https://graph.facebook.com/v19.0/ads_archive) <br>
- [ClawHub skill page](https://clawhub.ai/AdarshVMore/meta-ads-collector-adarsh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript interfaces and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns typed Meta ads metrics and graceful error details when collection fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
