## Description: <br>
Interact with WhatsApp via GOWA (Go WhatsApp Web Multi-Device) REST API for personal automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aldinokemal](https://clawhub.ai/user/aldinokemal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to draft REST API calls and operational guidance for sending WhatsApp messages, media, contacts, locations, polls, and managing groups through a local GOWA server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to operate a linked WhatsApp account through a local REST server, including sending messages and media. <br>
Mitigation: Install only when this account control is intended, keep the REST server bound to localhost on a trusted machine, and require explicit confirmation before sending messages or media. <br>
Risk: Group operations such as @everyone or ghost mentions, participant changes, admin changes, message edits, deletes, and logouts can disrupt users or groups. <br>
Mitigation: Require explicit confirmation before using @everyone or ghost mentions, reading or exporting chats and contacts, deleting or editing messages, changing group membership or admin settings, removing devices, or logging out. <br>
Risk: A default unauthenticated local REST endpoint may be reachable by other local processes or by an accidentally exposed network service. <br>
Mitigation: Enable Basic Auth when available, avoid exposing the service beyond localhost, and run it only on trusted machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aldinokemal/gowa) <br>
- [GOWA API Endpoints Reference](references/api-endpoints.md) <br>
- [GOWA GitHub repository](https://github.com/aldinokemal/go-whatsapp-web-multidevice) <br>
- [GOWA releases](https://github.com/aldinokemal/go-whatsapp-web-multidevice/releases) <br>
- [GOWA OpenAPI specification](https://raw.githubusercontent.com/aldinokemal/go-whatsapp-web-multidevice/refs/heads/main/docs/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides instructions and request examples; it does not include executable helper scripts.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
