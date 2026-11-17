## Description:

Authorize, read, triage, archive, trash, and summarize Gmail inboxes across multiple accounts using the Gmail API with OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

People managing multiple Gmail inboxes use this skill to authorize accounts, review messages, summarize inbox state, and apply triage actions such as archive, label, mark read, or trash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store long-lived Gmail refresh tokens locally.

Mitigation: Protect the secrets/inbox directory, keep token files out of commits and shared archives, and revoke Google OAuth access if a token may have been exposed.

Risk: The skill can archive, label, mark read, or trash Gmail messages across multiple accounts.

Mitigation: Require account-specific confirmation and a preview before any archive, label, mark-read, or trash action.

Risk: Bulk trash operations can affect many messages in one run.

Mitigation: Review Gmail query filters and batch previews before execution, especially when operating across multiple accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hohobohan/skills/hobohan-inbox-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/hohobohan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands, configuration paths, Gmail API request examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Gmail OAuth setup, local token files, inbox queries, triage actions, and cleanup rules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
