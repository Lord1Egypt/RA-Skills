## Description: <br>
Google Analytics API integration with managed OAuth for read-only Data API reporting and explicitly approved Admin API configuration changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent query GA4 reporting data through the Google Analytics Data API and, when explicitly needed, manage Google Analytics accounts, properties, and data streams through the Admin API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and brokered Google Analytics OAuth access, so the agent can act through the connected account. <br>
Mitigation: Install only if you trust Maton to broker access, keep MATON_API_KEY private, and revoke unused Google Analytics connections. <br>
Risk: Google Analytics Admin API actions can create, update, or delete accounts, properties, and data streams. <br>
Mitigation: Prefer read-only Data API reporting tasks and require explicit approval with resource identifiers and consequences before any Admin API write operation. <br>


## Reference(s): <br>
- [Google Analytics Admin API Overview](https://developers.google.com/analytics/devguides/config/admin/v1) <br>
- [Google Analytics Data API Overview](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [Google Analytics Skill on ClawHub](https://clawhub.ai/byungkyu/google-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, shell commands, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a Google Analytics OAuth connection through Maton; prefer Data API reporting workflows unless an admin change is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
