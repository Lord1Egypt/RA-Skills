## Description: <br>
Read and manage email via IMAP (ProtonMail Bridge, Gmail, etc.). Check for new/unread messages, fetch content, search mailboxes, and mark as read/unread. Works with any IMAP server including ProtonMail Bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvarrieur](https://clawhub.ai/user/mvarrieur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to connect to an IMAP mailbox, check unread or recent messages, fetch full message content, search mailboxes, and mark messages read or unread. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive mailbox data through IMAP credentials. <br>
Mitigation: Install only for mailboxes the agent is allowed to read or manage, and use a Bridge-generated or app-specific password where possible. <br>
Risk: Credentials stored in a local .env file can be exposed if file permissions or version-control exclusions are not handled carefully. <br>
Mitigation: Ensure .env is excluded from version control, restrict local file permissions, and rotate credentials if exposure is suspected. <br>
Risk: Disabling certificate validation can increase man-in-the-middle risk outside trusted local Bridge use. <br>
Mitigation: Keep certificate checks enabled for normal IMAP servers and set IMAP_REJECT_UNAUTHORIZED=false only for trusted local ProtonMail Bridge use. <br>
Risk: The cron example can send email summaries to an external messaging destination. <br>
Mitigation: Replace or avoid the example delivery target unless that destination is explicitly intended for the mailbox summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvarrieur/imap-email) <br>
- [Publisher profile](https://clawhub.ai/user/mvarrieur) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the IMAP CLI, with Markdown instructions and inline shell commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may include mailbox metadata, message headers, snippets, full text or HTML bodies, attachment metadata, and read/unread status results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
