## Description:

JSON校验工具专业版 helps agents validate JSON at enterprise scale with parallel scans, JSON Schema checks, JSON5/JSONC/JSON-LD/HJSON compatibility, repair suggestions, CI/CD integration, and monitoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, operations teams, and compliance reviewers use this skill to validate large JSON estates, enforce schema rules, inspect configuration quality, and produce structured findings or repair guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill asks agents to activate for unrelated project-management work.

Mitigation: Use this skill only for JSON validation workflows and ignore activation language outside that scope.

Risk: The security guidance notes under-scoped external notification behavior through webhook, email, or DingTalk callbacks.

Mitigation: Configure external callbacks only after confirming that validation results and file-derived metadata are acceptable to send to those services.

Risk: Automatic repair behavior can modify JSON files incorrectly or without sufficient review.

Mitigation: Keep auto-repair disabled unless backups are verified, restrict scans to intended directories, and review suggested fixes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-lint-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style validation reports with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, error locations, schema validation results, repair suggestions, progress logs, trend summaries, and alert configuration guidance.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
