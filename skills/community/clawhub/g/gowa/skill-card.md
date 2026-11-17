## Description:

Provides guidance and curl examples for using GOWA's local WhatsApp REST API to send messages, media, mentions, and manage groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aldinokemal](https://clawhub.ai/user/aldinokemal)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to interact with a local GOWA REST server for WhatsApp messaging, media delivery, status checks, and group administration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides use of a powerful local REST API for WhatsApp automation, including messaging, media download, logout, and group membership or admin changes.

Mitigation: Run the REST API only on a tightly controlled host, enable authentication, avoid exposing port 3000, and require explicit confirmation before high-impact actions.

Risk: Ghost mentions and @everyone-style notifications can create unwanted broad notifications or social misuse if sent automatically.

Mitigation: Require human confirmation before sending group-wide mentions and limit automation to approved recipients and groups.

Risk: Downloading private media or accessing chats and contacts can expose personal data.

Mitigation: Restrict access to trusted operators, confirm intent before media downloads, and avoid logging or retaining private content unless explicitly required.

## Reference(s):

- [GOWA API Endpoints Reference](references/api-endpoints.md)
- [GOWA OpenAPI Specification](https://raw.githubusercontent.com/aldinokemal/go-whatsapp-web-multidevice/refs/heads/main/docs/openapi.yaml)
- [GOWA GitHub Repository](https://github.com/aldinokemal/go-whatsapp-web-multidevice)
- [ClawHub Skill Page](https://clawhub.ai/aldinokemal/skills/gowa)
- [Publisher Profile](https://clawhub.ai/user/aldinokemal)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline curl and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces REST API usage guidance for a local GOWA server; it does not include executable helper scripts.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
