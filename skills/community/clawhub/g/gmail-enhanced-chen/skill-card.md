## Description: <br>
Enhanced Gmail integration with advanced features including label management, attachment handling, advanced search, email parsing, and automated email processing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to connect an agent to Gmail for advanced search, label management, attachment handling, email parsing, and rule-based email processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and modify Gmail messages automatically. <br>
Mitigation: Review rules before running automated processing, avoid broad auto-reply rules, and test first with a low-risk mailbox. <br>
Risk: The skill stores long-lived Gmail credential and token files on disk. <br>
Mitigation: Protect credential and token files, restrict file permissions, and rotate or revoke tokens if exposure is suspected. <br>
Risk: Downloaded attachments may introduce unwanted files into the local environment. <br>
Mitigation: Download attachments only into a controlled directory and review files before opening or forwarding them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jason-aka-chen/gmail-enhanced-chen) <br>
- [Gmail API Documentation](https://developers.google.com/gmail/api) <br>
- [OAuth Setup Guide](https://developers.google.com/gmail/api/quickstart/python) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Gmail API actions when used by an agent with configured OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
