## Description: <br>
Gmail email integration for reading, searching, sending, labeling, and managing messages through MorphixAI delegated Gmail API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to work with a linked Gmail account: inspect profile information, list and search messages, read message details, send plain-text email, list labels, mark messages as read, and move messages to trash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates access to a user's Gmail account through MorphixAI, which can expose email contents and account actions if connected to the wrong account or used without review. <br>
Mitigation: Install only if MorphixAI and the openclaw-morphixai plugin are trusted, link only the intended Gmail account, and review granted scopes before use. <br>
Risk: The skill can send email or move messages to trash through Gmail actions. <br>
Mitigation: Require clear user confirmation before sending messages or trashing email, and review action parameters before execution. <br>


## Reference(s): <br>
- [ClawHub Gmail skill page](https://clawhub.ai/paul-leo/gmail-2) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with shell commands and structured mx_gmail tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Gmail account; generated examples include Gmail actions such as list_messages, get_message, search_messages, send_mail, list_labels, mark_as_read, and trash_message.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
