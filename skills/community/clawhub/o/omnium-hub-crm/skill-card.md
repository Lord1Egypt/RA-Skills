## Description: <br>
Manage Omnium Hub CRM (contacts, opportunities, appointments). Use for all CRM-related tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omniumhub](https://clawhub.ai/user/omniumhub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and CRM operators use this skill to look up, create, and update Omnium Hub contacts and to list or create opportunities through a LeadConnector-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Omnium Hub CRM records when supplied with a compatible API key. <br>
Mitigation: Use a limited, revocable API key where possible and review create or update operations before running them. <br>
Risk: Supplying API keys directly in prompts or shell commands can expose credentials in logs or command history. <br>
Mitigation: Avoid placing the key in persistent chat or shell history, and rotate the key if exposure is suspected. <br>
Risk: The CRM client targets services.leadconnectorhq.com, which may not be the intended backend for every account. <br>
Mitigation: Verify that services.leadconnectorhq.com is the correct backend for the user's Omnium Hub account before use. <br>


## Reference(s): <br>
- [Omnium Hub CRM on ClawHub](https://clawhub.ai/omniumhub/omnium-hub-crm) <br>
- [LeadConnector-compatible API endpoint](https://services.leadconnectorhq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the CRM client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided Omnium Hub API key and prints API responses as formatted JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
