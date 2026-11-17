## Description:

Search, read, and manage DocuSign envelopes, recipients, templates, documents, and signing status through a local MCP wrapper. Use when the user asks about DocuSign signing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Users can inspect DocuSign envelopes, recipients, templates, documents, and signing status, and manage signing workflows through DocuSign tools. Confirm user intent before creating, sending, voiding, updating, or modifying agreements or related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending or modifying an envelope can affect a real signing workflow, and sending has no draft or preview stage.

Mitigation: Confirm the intended action, agreement, template, and recipients with the user; inspect relevant envelope details before making changes.

Risk: OAuth credentials grant access to the connected DocuSign account.

Mitigation: Connect the intended account and protect access to its stored OAuth credentials.

## Reference(s):

- [DocuSign skill release on ClawHub](https://clawhub.ai/maverick/skills/maverick-docusign-mcp)
- [mcporter](https://github.com/steipete/mcporter)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Text or structured JSON returned from DocuSign tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include envelope, recipient, template, document, and signing-status information; write actions can change real DocuSign records.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
