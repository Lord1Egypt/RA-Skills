## Description:

Automates publishing Toutiao articles and micro-posts, including topic selection, article drafting, image handling, cookie-based login, mixed text-image posting, scheduling, and Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin1220](https://clawhub.ai/user/kevin1220)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate, schedule, and publish Toutiao articles or micro-posts with images through a configured Toutiao account, then receive Feishu status notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Toutiao content using a logged-in account.

Mitigation: Use a dedicated account, test generation-only or non-publishing flows first, and require human review before enabling live publishing.

Risk: Session cookies and Feishu configuration can grant account or notification access if exposed.

Mitigation: Keep cookie and configuration files out of repositories and backups, restrict file permissions, and rotate cookies regularly.

Risk: Scheduled posting can repeat public publishing without timely oversight.

Mitigation: Avoid unattended scheduling until confirmation controls, monitoring, and rollback procedures are in place.

Risk: Browser automation interacts with a logged-in web session and may be affected by page changes or unexpected dialogs.

Mitigation: Run the browser in an isolated unprivileged environment with sandboxing enabled where possible and inspect logs or screenshots after test runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin1220/skills/kevin-toutiao-auto-publisher)
- [Toutiao publisher portal](https://mp.toutiao.com)
- [Toutiao article publishing page](https://mp.toutiao.com/profile_v4/graphic/publish)
- [Toutiao micro-post publishing page](https://mp.toutiao.com/profile_v4/weitoutiao/publish)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message send API](https://open.feishu.cn/open-apis/message/v4/send)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, generated publishing text, and execution guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local logs, screenshots, article drafts, micro-post text, image references, and Feishu notification status.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
