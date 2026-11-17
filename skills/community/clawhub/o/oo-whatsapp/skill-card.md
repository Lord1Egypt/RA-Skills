## Description:

WhatsApp (whatsapp.com). Use this skill for ANY WhatsApp request — reading, creating, updating, and deleting data. Whenever a task involves WhatsApp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve WhatsApp Business profile, phone number, template, media, and analytics data, and to send or manage messages, media, contacts, and templates through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run a remote installer, and the downloaded installer and CLI behavior were not fully verified.

Mitigation: Review setup before installing, prefer a CLI version you have reviewed, and require separate approval before running remote installers or making additional agent-skill changes.

Risk: WhatsApp requests pass through OOMOL, which has access to the connected account and handles its data.

Mitigation: Consider OOMOL's account access and data handling before connecting WhatsApp.

Risk: Sending messages or uploading media changes account state, and deleting a template removes its variants.

Mitigation: Confirm the exact payload and effect before messages or uploads, and get explicit approval for template deletions.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [WhatsApp Cloud API documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [WhatsApp](https://www.whatsapp.com)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls]

**Output Format:** [JSON action responses and WhatsApp messages or account updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read account data or change WhatsApp state; confirmation is required for sends, uploads, and deletions.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
