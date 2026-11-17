## Description:

Promote schedule details from Gmail into Google Calendar via Maton by reading Gmail messages, extracting structured or free-text event information, and creating Google Calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orulink](https://clawhub.ai/user/orulink)

### License/Terms of Use:

MIT

## Use Case:

People managing schedules from email use this skill to read Gmail messages, extract event details, and create matching Google Calendar events through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private Gmail and Calendar data through Maton and needs broad account authority.

Mitigation: Install only when comfortable with that access, keep Maton Gmail and Calendar connections limited to intended accounts, and review event payloads before writing.

Risk: MATON_API_KEY may be stored in a local .env file and examples may load it into shell commands.

Mitigation: Do not print or commit .env; use a safer secret store or tightly permissioned environment variable where possible.

Risk: Free-text extraction can misread dates, times, locations, or thread context.

Mitigation: Run with --dry-run first, confirm extracted fields and event payload, and avoid importing confidential thread history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orulink/skills/gmail-to-calendar)
- [Gmail API reference](https://developers.google.com/gmail/api/reference/rest)
- [Gmail messages list](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
- [Gmail messages get](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
- [Maton](https://maton.ai)
- [Maton support](mailto:support@maton.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples; the helper script emits JSON results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATON_API_KEY plus active Maton google-mail and google-calendar connections.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
