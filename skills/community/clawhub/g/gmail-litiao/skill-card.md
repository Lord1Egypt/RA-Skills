## Description: <br>
Gmail API integration with managed OAuth for reading, sending, and managing emails, threads, labels, and drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Gmail through Maton-managed OAuth so it can inspect mail, manage labels and threads, draft messages, and send email through authenticated Gmail API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives a third-party gateway and an agent access to Gmail content and mailbox actions through MATON_API_KEY. <br>
Mitigation: Install only when the user trusts Maton with Gmail access, use the user's own MATON_API_KEY, and revoke the OAuth connection when access is no longer needed. <br>
Risk: Supported actions include sending mail, trashing messages, changing labels, creating drafts, and deleting OAuth connections. <br>
Mitigation: Require explicit user confirmation before sending email, trashing messages, applying label changes in bulk, sending drafts, or deleting connections. <br>
Risk: The examples include a connection UUID that could be copied accidentally. <br>
Mitigation: Replace example identifiers with the user's own connection ID before executing requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/gmail-litiao) <br>
- [Maton](https://maton.ai) <br>
- [Maton Connection Management](https://ctrl.maton.ai) <br>
- [Gmail API Overview](https://developers.google.com/gmail/api/reference/rest) <br>
- [Gmail API Users Messages](https://developers.google.com/gmail/api/reference/rest/v1/users.messages) <br>
- [Gmail API Users Drafts](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an authorized Gmail connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
