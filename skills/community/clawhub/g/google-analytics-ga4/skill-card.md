## Description: <br>
Query Google Analytics GA4 properties for realtime and historical user metrics, dimensions, and metadata using the official Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Whosc](https://clawhub.ai/user/Whosc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics operators use this skill to configure service-account access and run command-line GA4 realtime, historical, and metadata queries. It supports Markdown reports by default and optional JSON output for downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires read access to the selected GA4 property through a service-account key. <br>
Mitigation: Use a dedicated service account with the minimum Viewer role and grant access only to intended GA4 properties. <br>
Risk: A leaked service-account JSON key could expose analytics data to unauthorized users. <br>
Mitigation: Keep the key out of shared folders and repositories, and rotate it immediately if exposed. <br>
Risk: Optional DingTalk delivery can send analytics reports to external chat channels. <br>
Mitigation: Set DingTalk webhook variables only for channels approved to receive the relevant analytics data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Whosc/google-analytics-ga4) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [GA4 dimensions and metrics schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) <br>
- [Google Analytics Data API Python client](https://github.com/googleapis/google-analytics-data-python) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables by default, optional JSON responses, shell command examples, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GA4 property ID and Google service-account credentials; optional DingTalk delivery uses approved webhook environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
