## Description:

Use when using Mailtrap Contacts API or UI to add, update, bulk import, list, segment marketing contacts, custom fields, or custom events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and operations teams use this skill to manage Mailtrap marketing contacts, lists, custom fields, custom events, imports, exports, and CRM or warehouse sync workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailtrap contacts may include personal data, and bulk imports, deletes, or exports can affect many records.

Mitigation: Use a least-privilege Mailtrap token, confirm the target account and list, and require explicit approval before bulk operations.

Risk: Contact-management guidance can be applied to the wrong Mailtrap account, list, or contact segment.

Mitigation: Verify the Mailtrap account ID, list IDs, and intended audience before generating or executing API requests.

## Reference(s):

- [Managing contacts skill page](https://clawhub.ai/mailtrap/skills/managing-contacts)
- [Mailtrap Contacts OpenAPI spec](https://github.com/mailtrap/mailtrap-openapi/blob/main/specs/contacts.openapi.yml)
- [Mailtrap contacts API](https://docs.mailtrap.io/developers/promotional/contacts/contacts.md)
- [Mailtrap bulk import contacts](https://docs.mailtrap.io/developers/promotional/contacts/bulk-import.md)
- [Mailtrap contact lists](https://docs.mailtrap.io/developers/promotional/contacts/contact-lists.md)
- [Mailtrap contact fields](https://docs.mailtrap.io/developers/promotional/contacts/contact-fields.md)
- [Mailtrap contact events](https://docs.mailtrap.io/developers/promotional/contacts/contact-events.md)
- [Mailtrap export contacts](https://docs.mailtrap.io/developers/promotional/contacts/export-contacts.md)
- [Mailtrap import contacts](https://docs.mailtrap.io/email-marketing/contacts/import-contacts.md)
- [Mailtrap suppressions](https://docs.mailtrap.io/developers/email-sending/suppressions.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline curl examples and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Mailtrap account IDs, API tokens, list IDs, custom fields, and contact identifiers supplied by the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
