## Description: <br>
Extended Google Workspace CLI reference for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. Includes complete email body retrieval, attachments, and advanced query patterns. Use when working with Gmail to read full email content, extract attachments, search with advanced filters, or manage Google Workspace documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethanyanjiali](https://clawhub.ai/user/ethanyanjiali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to operate the gog CLI for Google Workspace tasks, especially retrieving complete Gmail bodies, extracting attachments, searching messages, and working with Calendar, Drive, Contacts, Sheets, and Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward broad Google Workspace access across email, calendar, contacts, documents, and spreadsheets. <br>
Mitigation: Install only when the gog CLI is trusted, grant the minimum Google services needed, and confirm the active account before use. <br>
Risk: Write, send, delete, clear, or bulk operations can change or expose user data if run without review. <br>
Mitigation: Require approval before those operations and avoid --no-input for write, send, delete, clear, or bulk data commands. <br>
Risk: Email body and document retrieval may expose sensitive personal or business information. <br>
Mitigation: Use specific account and query filters, prefer structured output for controlled parsing, and review retrieved content before downstream automation. <br>


## Reference(s): <br>
- [Email Extraction Patterns](references/email-extraction-patterns.md) <br>
- [GOG CLI Homepage](https://gogcli.sh) <br>
- [ClawHub Release Page](https://clawhub.ai/ethanyanjiali/gog-extended) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for account selection, read operations, writes, exports, and script-oriented JSON output.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
