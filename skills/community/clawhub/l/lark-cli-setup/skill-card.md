## Description:

Guides an agent through installing lark-cli, completing Feishu/Lark user authorization, configuring token refresh, and validating access to Feishu/Lark workspace features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingshang2024-cell](https://clawhub.ai/user/jingshang2024-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workspace users use this skill to connect an agent to Feishu/Lark by installing lark-cli, completing account authorization, setting up refresh behavior, and checking document, calendar, mail, message, wiki, approval, and related access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Feishu/Lark account access across documents, mail, messages, calendars, approvals, and other business data.

Mitigation: Install only when broad workspace access is intended, and prefer limiting domains or permissions to the minimum needed where the CLI and organization policy allow it.

Risk: The skill creates ongoing token refresh behavior, which can preserve agent access after initial authorization.

Mitigation: Create the refresh schedule only after confirming how to disable it, revoke authorization, and rotate or remove tokens if access is no longer needed.

Risk: The install command fetches lark-cli globally through npm using an external registry mirror.

Mitigation: Prefer a pinned, reviewed, or locally controlled lark-cli installation source before using the skill in sensitive environments.

## Reference(s):

- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide QR-code generation for authorization and creation of a recurring token-refresh schedule.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
