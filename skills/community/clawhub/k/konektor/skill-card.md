## Description: <br>
Access and manage marketing leads, update lead details, and retrieve analytics for lead performance and conversion tracking via the Konektor API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RamaAditya49](https://clawhub.ai/user/RamaAditya49) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, sales, and operations teams use this skill through agents to retrieve and manage Konektor leads, review campaign and conversion analytics, inspect workspace information, and create support tickets through the Konektor API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Konektor lead, workspace, analytics, and conversion data through an external API. <br>
Mitigation: Install it only where that data access is intended, use a dedicated least-privilege API key, and prefer read-only scopes unless write operations are required. <br>
Risk: Lead creation, lead updates, and support ticket creation can submit personal or sensitive business information. <br>
Mitigation: Require user confirmation before write operations and review payloads before sending them to Konektor. <br>
Risk: API keys are bearer tokens and can grant scoped access to workspace data. <br>
Mitigation: Store KONEKTOR_API_KEY in the agent environment, avoid exposing it in prompts or logs, and rotate or revoke keys that are no longer needed. <br>


## Reference(s): <br>
- [Konektor Agent API Documentation](https://konektor.id/docs/api/agent-api) <br>
- [ClawHub Skill Listing](https://clawhub.ai/RamaAditya49/konektor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Configuration] <br>
**Output Format:** [Markdown with endpoint tables, JSON examples, and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HTTPS JSON requests authenticated with a scoped KONEKTOR_API_KEY.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
