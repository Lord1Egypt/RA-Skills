## Description:

Agent email via JSON API. Use when sending/receiving email as an agent, checking inbox, or working with the OctoMail service (@octomail.ai addresses).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonz-ncc42](https://clawhub.ai/user/jasonz-ncc42)

### License/Terms of Use:


## Use Case:

Developers and agent operators use OctoMail to register an agent email identity, send and receive OctoMail messages, poll inboxes, read messages, download attachments, and manage invitation or sponsor-link flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OctoMail API keys authorize agent email access.

Mitigation: Protect OCTOMAIL_API_KEY and avoid exposing it in logs, prompts, shared files, or message bodies.

Risk: Messages and attachments may contain sensitive or unintended information.

Mitigation: Verify recipients before sending, avoid sending secrets unless appropriate, and save downloaded attachments only to controlled paths.

Risk: The unlink sponsor endpoint changes account linkage.

Mitigation: Use the unlink operation only when the account-linking impact is intended and understood.

## Reference(s):

- [OctoMail homepage](https://octomail.ai)
- [OctoMail OpenAPI schema](https://api.octomail.ai/v1/openapi.json)
- [ClawHub skill page](https://clawhub.ai/jasonz-ncc42/skills/octomail)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OCTOMAIL_API_KEY for authenticated requests.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
