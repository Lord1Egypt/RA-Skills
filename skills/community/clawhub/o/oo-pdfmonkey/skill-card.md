## Description:

PDFMonkey (pdfmonkey.io). Use this skill for ANY PDFMonkey request — reading, creating, and updating data. Whenever a task involves PDFMonkey, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to read PDFMonkey account, document, and template data, and to create PDFMonkey documents through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute remote code and make broader persistent agent changes without clear user approval.

Mitigation: Review and install a trusted CLI release separately before enabling the skill; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: OOMOL mediates PDFMonkey data and account access.

Mitigation: Review the account connection and understand what PDFMonkey data and actions are available through it.

## Reference(s):

- [PDFMonkey](https://pdfmonkey.io)
- [PDFMonkey API authentication documentation](https://pdfmonkey.io/docs/api/authentication/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action dependent; write actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
