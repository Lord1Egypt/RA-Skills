## Description:

Extended Google Workspace CLI reference for Gmail, Calendar, Drive, Contacts, Sheets, and Docs, including complete email body retrieval, attachments, and advanced query patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethanyanjiali](https://clawhub.ai/user/ethanyanjiali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for practical `gog` CLI guidance for Gmail and Google Workspace workflows, including reading full email content, extracting attachments, searching messages, and managing Calendar, Drive, Contacts, Sheets, and Docs commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide sensitive Google Workspace actions such as sending email, downloading attachments, changing calendars, and modifying or clearing Sheets.

Mitigation: Use only authorized Google accounts and services, prefer narrow OAuth scopes, and require explicit confirmation before account-changing or data-export actions.

Risk: The artifact includes real-looking personal email and order examples that could create a privacy issue if reused.

Mitigation: Do not reuse the examples in workflows; replace them with sanitized test data or user-provided values.

## Reference(s):

- [Email Extraction Patterns](references/email-extraction-patterns.md)
- [gog CLI homepage](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples for authorized Google Workspace accounts and services.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
