## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Gog to access and manage Gmail, Calendar, Drive, Contacts, Sheets, and Docs from shell commands. The guide covers OAuth setup and common Workspace tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth authorization can grant access to the selected Google Workspace services, including operations that send messages or change data.

Mitigation: Review and limit the requested services and scopes, and confirm before sending messages or making changes. Keep credentials and callback URLs in the trusted shell rather than chat.

Risk: The security assessment is incomplete because two referenced message files were unavailable.

Mitigation: Review the requested account access and setup steps before installing, as advised by the security assessment.

## Reference(s):

- [Gog CLI](https://gogcli.sh)
- [Gog on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-gog)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or modify Google Workspace data according to the requested task.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
