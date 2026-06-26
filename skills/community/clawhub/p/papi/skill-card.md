## Description: <br>
Complete WhatsApp automation API with microservices architecture. Send messages, interactive buttons, lists, carousels, polls, manage instances, groups, catalogs and webhooks. Features Admin Panel (free), Phone Calls, RCS Messaging, SMS, Virtual Numbers (Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafacpti23](https://clawhub.ai/user/rafacpti23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate PAPI-based WhatsApp automation, including instance management, message sending, groups, catalogs, webhooks, WebSockets, and customer-service integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-assisted messaging, group operations, and catalog changes can affect WhatsApp recipients or business data. <br>
Mitigation: Approve message sends, group membership changes, and catalog updates deliberately before using generated API requests. <br>
Risk: The PAPI API key grants access to automation endpoints. <br>
Mitigation: Keep the API key private and avoid placing it in shared prompts, logs, or public configuration. <br>
Risk: Webhook and WebSocket destinations may receive WhatsApp event data. <br>
Mitigation: Configure only trusted HTTPS or WSS destinations that are approved to receive that data. <br>


## Reference(s): <br>
- [PAPI official website](https://papi.api.br) <br>
- [PAPI ClawHub listing](https://clawhub.ai/rafacpti23/papi) <br>
- [Interactive messages reference](artifact/references/interactive.md) <br>
- [Groups reference](artifact/references/groups.md) <br>
- [Catalog reference](artifact/references/catalog.md) <br>
- [Integrations reference](artifact/references/integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage guidance for PAPI/WhatsApp automation; does not execute requests by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
