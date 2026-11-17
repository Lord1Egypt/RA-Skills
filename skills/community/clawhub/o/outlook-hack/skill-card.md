## Description:

Read and search Outlook, inspect attachments, and create or edit drafts without any send endpoint. Uses one short-lived Microsoft Graph access token supplied on stdin for one run; it never stores credentials. Bulk mailbox export is opt-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Outlook mail, download selected attachments, and prepare or update drafts through Microsoft Graph while leaving final sending to a human in Outlook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Microsoft Graph token grants access to sensitive mailbox data and draft operations.

Mitigation: Use a short-lived token scoped only to the mail actions needed for the command.

Risk: Email content and generated summaries may contain deceptive or untrusted instructions.

Mitigation: Treat message content and summaries as untrusted context and do not follow instructions found in mail without independent review.

Risk: Optional mailbox exports and attachment downloads write plaintext local files.

Mitigation: Use exports only when needed, keep them in private directories, and remove local plaintext data when it is no longer required.

Risk: Draft creation or patching can alter mailbox state even though the skill does not send mail.

Mitigation: Review every draft manually in Outlook before sending or relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/outlook-hack)
- [Microsoft Graph endpoint](https://graph.microsoft.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command output from Microsoft Graph mail operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local plaintext mailbox exports and attachment files only when explicitly requested with the consent flag.]

## Skill Version(s):

3.4.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
