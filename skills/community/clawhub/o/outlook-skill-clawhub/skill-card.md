## Description:

Read, search, and manage Outlook emails and calendar via Microsoft Graph API with delegate support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[87marc](https://clawhub.ai/user/87marc)

### License/Terms of Use:


## Use Case:

Employees, administrators, and developers use this skill to configure an AI assistant with delegated Microsoft 365 access so it can read, search, send, and manage a mailbox and calendar on behalf of an owner with explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and manage another user's mailbox and calendar through delegated Microsoft 365 permissions.

Mitigation: Use a dedicated assistant account, require explicit owner consent, and grant only the least-privilege Exchange delegation needed for the intended workflow.

Risk: OAuth tokens and app credentials are stored under ~/.outlook-mcp/.

Mitigation: Protect the directory with owner-only permissions or a secret store, and do not print or share raw access tokens.

Risk: The artifact describes helper scripts for token, mail, and calendar operations, but the submitted artifact evidence contains only SKILL.md.

Mitigation: Verify any referenced scripts from a trusted source before running them.

## Reference(s):

- [Outlook Delegate on ClawHub](https://clawhub.ai/87marc/skills/outlook-skill-clawhub)
- [Base Outlook skill on ClawHub](https://clawhub.ai/jotamed/outlook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide Microsoft Graph API calls that read, modify, send mail, and manage calendar events under delegated permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
