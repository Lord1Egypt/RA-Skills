## Description: <br>
Summarizes the latest NicheStarter weekly pain-point report from the public preview API, lists top five pain points, and guides users to sign in for the full report and free weekly email subscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shujip](https://clawhub.ai/user/shujip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch NicheStarter's public weekly preview, produce a concise top-five pain-point digest, and guide readers to the full signed-in report or free weekly email subscription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled delivery can send stale or duplicate digests if the same report is fetched more than once. <br>
Mitigation: Persist only the last sent report ID and skip delivery when the public API returns the same report ID. <br>
Risk: Notification channels may require separate credentials outside this skill. <br>
Mitigation: Configure recipients and channels explicitly, protect notification credentials separately, and keep this skill limited to public preview fetching and digest formatting. <br>
Risk: The digest summarizes community signals and may be mistaken for guaranteed demand. <br>
Mitigation: Present pain points as community signal only and avoid inventing rankings, counts, or paid-only capabilities. <br>
Risk: The public preview API may be unavailable or return no current report. <br>
Mitigation: Use the documented fallback message for 404 or empty responses and do not fabricate report content. <br>


## Reference(s): <br>
- [Weekly report preview API reference](reference.md) <br>
- [NicheStarter public weekly report preview API](https://www.nichestarter.ai/api/public/weekly-report-preview) <br>
- [NicheStarter website](https://www.nichestarter.ai) <br>
- [NicheStarter public insights](https://www.nichestarter.ai/insights) <br>
- [ClawHub skill page](https://clawhub.ai/shujip/painpoint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest with optional plain-text links and scheduler examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only the public preview API response; scheduled delivery should deduplicate by report ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
