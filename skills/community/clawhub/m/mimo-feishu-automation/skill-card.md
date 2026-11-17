## Description:

飞书自动化工具 helps agents produce Chinese Feishu automation plans and code-oriented guidance for scheduled messages, reports, Bitable operations, calendar events, and approval workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workplace automation owners use this skill to draft Chinese Feishu automation workflows, permissions, API calls, schedules, and output templates for messages, reports, Bitable records, calendar events, and approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers powerful Feishu workplace actions using app credentials and broad API scopes.

Mitigation: Use a Feishu app with carefully limited scopes, keep scheduled automations narrowly scoped and auditable, and validate target record, event, task, and recipient IDs before execution.

Risk: The artifact includes token-printing examples and token handling patterns.

Mitigation: Remove token-printing examples before production use and store App Secret and tokens in environment variables or encrypted secret storage.

Risk: The skill includes destructive or high-impact actions such as batch deletion, approval decisions, and scheduled automation.

Mitigation: Require explicit confirmation for deletes and approval decisions, add request validation, and review workflows before enabling production schedules.

Risk: Feishu APIs have permission and rate-limit constraints that can cause failed or excessive automation.

Mitigation: Confirm administrator approval for required permissions, apply rate limiting or retry spacing, and monitor automation logs with sensitive values redacted.

## Reference(s):

- [飞书自动化工具 - 详细内容](artifact/references/details.md)
- [Feishu Open Platform App Console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown with Python examples, Feishu API payloads, Cron expressions, and configuration checklists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as plans and examples; executing API actions requires separately configured Feishu credentials and scopes.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
