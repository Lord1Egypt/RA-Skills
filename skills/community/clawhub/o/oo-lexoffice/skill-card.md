## Description:

lexoffice (office.lexware.de). Use this skill for ANY lexoffice request — reading, creating, and updating data. Whenever a task involves lexoffice, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting operators and assistants use this skill to read Lexoffice articles, contacts, vouchers, and profile information, and to create or update articles and contacts through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run downloaded installer code without separate approval, including automatic skill synchronization.

Mitigation: Review and separately approve the CLI installation and synchronization; prefer a pinned, independently verified installer. Confirm accounting changes before execution.

## Reference(s):

- [Lexoffice API documentation](https://developers.lexoffice.io/)
- [Lexoffice homepage](https://office.lexware.de/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-lexoffice)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON responses, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve account data; create and update actions change Lexoffice records and require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
