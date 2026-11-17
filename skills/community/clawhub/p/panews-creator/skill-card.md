## Description:

Create and manage articles on the PANews platform with authenticated creator workflows for drafting, publishing, revising, image uploads, tag search, column applications, and article review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medz](https://clawhub.ai/user/medz)

### License/Terms of Use:

MIT-0

## Use Case:

External PANews contributors and their agents use this skill to prepare, manage, and submit PANews articles through authenticated creator workflows, including drafts, revisions, media uploads, tag lookup, and column applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valid PANews session can let an agent create, update, submit, upload for, apply to, or delete creator content.

Mitigation: Use a secure credential source, keep the session narrowly controlled, and manually confirm each high-impact action before execution.

Risk: Deletion, submission, or update commands can affect the wrong article if IDs or status changes are not checked.

Mitigation: Confirm article IDs, target columns, requested field changes, and submit/delete intent with the user before taking the action.

Risk: Passing session tokens as command-line arguments can expose credentials through shell history or process listings.

Mitigation: Prefer environment variables, direnv, or a secret manager for PANews session values.

## Reference(s):

- [Publish a New Article](references/workflow-publish.md)
- [Manage My Articles](references/workflow-manage.md)
- [Revise and Resubmit](references/workflow-revise.md)
- [Apply for a Column](references/workflow-apply-column.md)
- [Polish an Article](references/workflow-polish.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use authenticated PANews creator actions when the user provides a valid session; article polishing can be text-only.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
