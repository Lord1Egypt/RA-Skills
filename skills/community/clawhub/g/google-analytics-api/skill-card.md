## Description: <br>
Google Analytics API integration with managed OAuth for managing accounts, properties, and data streams through the Admin API and running reports on sessions, users, page views, and conversions through the Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rich-song](https://clawhub.ai/user/rich-song) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to configure Maton-managed OAuth connections and issue Google Analytics Admin and Data API requests for GA4 account administration and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key for authentication. <br>
Mitigation: Protect MATON_API_KEY as a secret and avoid exposing it in shared commands, logs, or transcripts. <br>
Risk: Admin API requests can modify Google Analytics accounts, properties, data streams, custom dimensions, and conversion events. <br>
Mitigation: Verify account IDs, property IDs, request bodies, and intended connection before making administrative changes. <br>
Risk: Deleting a Maton connection can disrupt Google Analytics access for subsequent requests. <br>
Mitigation: Confirm the connection ID and expected impact before issuing DELETE requests. <br>


## Reference(s): <br>
- [Google Analytics Admin API Overview](https://developers.google.com/analytics/devguides/config/admin/v1) <br>
- [Google Analytics Data API Overview](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [Run Report API Reference](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport) <br>
- [Realtime Report API Reference](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runRealtimeReport) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and GA4 properties; Admin API and Data API access use separate OAuth connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
