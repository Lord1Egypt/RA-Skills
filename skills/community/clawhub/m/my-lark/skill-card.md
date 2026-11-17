## Description:

my-lark helps agents use Feishu/Lark messaging, groups, documents, Drive, Wiki, Calendar, approvals, Bitable, Sheets, whiteboards, and contacts through guided commands and API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longsasasasasa](https://clawhub.ai/user/longsasasasasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business automation users use this skill to configure Feishu/Lark access and automate collaboration workflows such as sending messages, searching documents, managing calendars, submitting approvals, and updating business tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports embedded app credentials.

Mitigation: Remove hard-coded App ID and App Secret values, rotate the exposed secret, and use externally managed credentials before real use.

Risk: The security assessment reports broad business-account access without adequate safeguards or disclosure.

Mitigation: Grant only required Feishu/Lark scopes, review permissions with an administrator, and require explicit confirmation before write, send, create, delete, public, or otherwise sensitive actions.

Risk: The security guidance flags token file handling.

Mitigation: Store token files with restricted permissions outside shared locations and avoid using real Feishu credentials until token storage is secured.

Risk: The security guidance flags unpinned dependencies.

Mitigation: Pin dependency versions and review dependency provenance before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longsasasasasa/skills/my-lark)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu OAuth access token documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/authen-v1/oidc-access-token/create)
- [Quick start](references/start-here.md)
- [Tool index](references/tools-index.md)
- [Authentication and permissions](references/auth.md)
- [Error codes](references/errors.md)
- [Messaging and groups API](references/im.md)
- [Drive and file API](references/drive.md)
- [Wiki API](references/wiki.md)
- [Document API](references/docx.md)
- [Sheets API](references/sheets.md)
- [Bitable API](references/bitable.md)
- [Board API](references/board.md)
- [Contact API](references/contact.md)
- [Calendar API](references/calendar.md)
- [Approval API](references/approval.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper commands may return JSON API responses from Feishu/Lark services when executed.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
