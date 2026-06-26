## Description: <br>
Helps an agent draft, send, read, search, and archive email using SMTP and IMAP with reusable templates and local draft storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users can use this skill to prepare templated email drafts, send messages through configured SMTP, inspect recent IMAP inbox messages, and manage local draft records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox content and send email through configured IMAP and SMTP accounts. <br>
Mitigation: Use a dedicated or least-privileged mailbox or app password, and review recipients, subject, and body before sending. <br>
Risk: Draft message bodies and recipient details are persisted locally in email_drafts.json. <br>
Mitigation: Avoid storing sensitive message bodies in drafts and delete email_drafts.json when the drafts are no longer needed. <br>
Risk: Email credentials are provided to the SMTP and IMAP helpers during use. <br>
Mitigation: Use app passwords or scoped credentials where available, and avoid embedding long-lived account passwords in shared files or transcripts. <br>


## Reference(s): <br>
- [Email Helper Pro on ClawHub](https://clawhub.ai/534422530/laosi-email-helper) <br>
- [Publisher profile 534422530](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with embedded Python code, YAML-style configuration examples, and JSON-like status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send SMTP messages, read IMAP inbox content, and persist local draft records in email_drafts.json.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, SKILL.md frontmatter, hub.json, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
