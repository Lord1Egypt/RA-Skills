## Description:

Generate a clean WhatsApp pairing QR code PNG from a running OpenClaw agent and deliver it to the user through the active conversation channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanblanchfield](https://clawhub.ai/user/seanblanchfield)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when an agent needs to start a WhatsApp device-linking flow, generate the short-lived pairing QR as a PNG, and send it back through the current channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill initiates a WhatsApp device-linking session after user confirmation.

Mitigation: Require explicit user readiness before running the QR generation command, and treat the resulting QR as short-lived account-linking material.

Risk: Mattermost thread delivery reads a stored bearer token from local OpenClaw configuration and uses direct API calls to upload and post the QR.

Mitigation: Use a brokered or narrowly scoped messaging tool where available; otherwise restrict and rotate the Mattermost token used for this workflow.

Risk: The QR code expires quickly, and delays can cause failed or repeated linking attempts.

Mitigation: Start the generation script immediately after confirmation and tell the user the process takes about 25 to 28 seconds before the roughly 60-second scan window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanblanchfield/skills/jentic-whatsapp-qr)
- [Mattermost file upload endpoint used by the skill](https://mattermost.claw.jentic.ai/api/v4/files)
- [Mattermost posts endpoint used by the skill](https://mattermost.claw.jentic.ai/api/v4/posts)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown instructions with bash and Python snippets; the runtime workflow produces a PNG QR code file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The QR code is time-sensitive, with artifact guidance stating it expires in about 60 seconds and the capture script takes about 25 to 28 seconds.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata, released 2026-03-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
