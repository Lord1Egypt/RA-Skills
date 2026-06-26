## Description: <br>
HubLinkPro GoHighLevel API helps agents manage contacts, pipelines, workflows, and messaging for Tri-Cities real estate lead generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbright4497](https://clawhub.ai/user/mbright4497) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate operations teams and their agents use this skill to prepare GoHighLevel API calls for lead intake, contact updates, pipeline opportunity work, notes, workflow triggers, and SMS follow-up for Tri-Cities campaigns. <br>

### Deployment Geography for Use: <br>
United States (Tri-Cities, Tennessee use case) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change GoHighLevel CRM records, opportunities, tags, notes, and workflows when commands are run. <br>
Mitigation: Use a least-privilege API key, protect environment variables, verify contact, opportunity, pipeline, and workflow IDs, and require human confirmation before write actions. <br>
Risk: The SMS command can send messages to contacts. <br>
Mitigation: Confirm recipient consent, message content, and applicable messaging rules before sending SMS. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbright4497/hlp-ghl-api) <br>
- [Publisher profile](https://clawhub.ai/user/mbright4497) <br>
- [LeadConnector API base URL](https://services.leadconnectorhq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with curl and jq command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GHL_API_KEY and GHL_LOCATION_ID; commands call the LeadConnector/GoHighLevel API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
