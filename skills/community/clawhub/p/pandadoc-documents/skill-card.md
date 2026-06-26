## Description: <br>
Create and manage PandaDoc documents, templates, folders, contacts, and signing workflows via the PandaDoc API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to PandaDoc through ClawLink, create documents from templates or uploads, manage templates, folders, and contacts, and track document signing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to the user's PandaDoc account through ClawLink. <br>
Mitigation: Install only when the user intends to connect PandaDoc through ClawLink, and review the requested PandaDoc permissions during connection. <br>
Risk: Write or destructive actions can create, update, move, send, or delete PandaDoc resources. <br>
Mitigation: Confirm the target resource and intended effect before executing any create, update, move, send, or delete action. <br>
Risk: Document sending and workflow triggers can affect external recipients. <br>
Mitigation: Preview the document, recipients, and workflow action with the user before sending or triggering a document workflow. <br>
Risk: Webhook creation can subscribe external endpoints to PandaDoc events. <br>
Mitigation: Confirm the webhook endpoint, event scope, and business purpose before creating a webhook subscription. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hith3sh/pandadoc-documents) <br>
- [PandaDoc API Documentation](https://developers.pandadoc.com/) <br>
- [PandaDoc Document API](https://developers.pandadoc.com/reference/documents) <br>
- [PandaDoc Template API](https://developers.pandadoc.com/reference/templates) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected PandaDoc account through ClawLink; write, destructive, sending, and webhook actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
