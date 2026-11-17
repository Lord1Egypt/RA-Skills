## Description:

Query Google Analytics GA4 properties for realtime and historical user metrics, dimensions, and metadata using the official Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whosc](https://clawhub.ai/user/whosc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to run GA4 realtime, historical, metadata, and traffic-source queries from an agent or shell workflow. It helps inspect site and product analytics through Markdown tables, JSON responses, and generated report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service-account credentials can expose GA4 data if stored in the skill directory or committed to source control.

Mitigation: Use a narrowly scoped Viewer service account, keep the JSON key outside the skill when possible, and apply ignore and secret-scanning protections.

Risk: Analytics reports can be sent to an arbitrary DingTalk webhook when webhook environment variables are configured.

Mitigation: Set DINGTALK_WEBHOOK only after verifying the destination and confirming that the report content is acceptable to send there.

## Reference(s):

- [GA4 Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 dimensions and metrics schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [GA4 Data API authorization](https://developers.google.com/analytics/devguides/reporting/data/v1/authorization)
- [Google Analytics Data API Python client](https://github.com/googleapis/google-analytics-data-python)
- [ClawHub skill page](https://clawhub.ai/whosc/skills/google-analytics-ga4)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables by default, optional JSON, generated Markdown reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GA4 property ID and Google service-account credentials or application default credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
