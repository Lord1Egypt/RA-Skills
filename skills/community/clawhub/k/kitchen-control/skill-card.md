## Description: <br>
Manage freezer inventory through WhatsApp commands, including stock tracking, expiration-aware scheduling, sales logging, dynamic pricing, and AI-assisted demand forecasting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[M3D3L](https://clawhub.ai/user/M3D3L) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers use this skill to route WhatsApp inventory, sales, and schedule commands into a PocketBase-backed freezer inventory workflow. It helps track stock levels, expiration dates, sales records, pricing adjustments, and demand forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change business records from WhatsApp messages using an admin PocketBase login without enforcing the claimed authorization. <br>
Mitigation: Deploy only behind an authenticated WhatsApp webhook, replace the admin login with a least-privilege service account, and add sender allowlists or role checks before enabling state-changing commands. <br>
Risk: Inventory, sales, and forecasting workflows may expose business data to PocketBase or external AI services. <br>
Mitigation: Document what data is stored or sent externally and validate the AI API endpoint, credentials, retention, and access controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/M3D3L/kitchen-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [WhatsApp-formatted text responses and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing inventory and sales operations require configured PocketBase and WhatsApp webhook integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
