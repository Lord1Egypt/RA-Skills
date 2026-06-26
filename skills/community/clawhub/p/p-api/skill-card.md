## Description: <br>
Automate WhatsApp messaging, interactive content, instance and group management, catalogs, and webhooks through the P-API service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafacpti23](https://clawhub.ai/user/rafacpti23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation teams use this skill to configure an agent for WhatsApp messaging, interactive messages, instance lifecycle tasks, group and catalog management, and webhook or integration setup through P-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected API key may allow an agent to send real WhatsApp messages. <br>
Mitigation: Use a limited-scope API key and require explicit approval before sending messages. <br>
Risk: Instance deletion, group changes, and catalog edits can alter service state. <br>
Mitigation: Test against a non-production instance first and require explicit approval for destructive or administrative actions. <br>
Risk: Webhook and integration setup can forward conversation events to external systems. <br>
Mitigation: Use trusted HTTPS endpoints, verify the destination owner, and restrict forwarded event types to what is needed. <br>


## Reference(s): <br>
- [P-API ClawHub listing](https://clawhub.ai/rafacpti23/p-api) <br>
- [P-API official website](https://papi.api.br) <br>
- [Interactive message reference](references/interactive.md) <br>
- [Group management reference](references/groups.md) <br>
- [Catalog reference](references/catalog.md) <br>
- [Integration reference](references/integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with endpoint examples, JSON request bodies, and curl snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; live actions require a user-supplied P-API base URL, API key, and instance.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
