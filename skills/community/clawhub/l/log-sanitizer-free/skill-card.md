## Description: <br>
扫描日志文件本地识别并脱敏密码、令牌、密钥等六类敏感信息，支持正则与关键词匹配，保障数据零外泄。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations engineers, and testers use this skill to scan local log files or directories, redact sensitive values such as passwords, API tokens, keys, and PII, and prepare safer logs for CI checks, archiving, audit, or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In-place redaction can irreversibly alter logs or hide useful debugging context. <br>
Mitigation: Run preview mode first, review findings, and keep original logs only in appropriately protected storage until redaction is verified. <br>
Risk: Generated .bak backup files may still contain sensitive log data. <br>
Mitigation: Treat backups as sensitive files and delete or secure them after confirming the redacted output. <br>
Risk: The inspected package references a log-sanitizer.py script that was not included in the artifact. <br>
Mitigation: Verify any external script source and behavior before executing commands against sensitive logs. <br>
Risk: The optional callback_url field could expose completion data if it sends sensitive status or metadata. <br>
Mitigation: Avoid callback_url unless the endpoint and payload are reviewed and limited to non-sensitive completion status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/log-sanitizer-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash and YAML snippets, plus optional text or JSON scan reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-selected log paths and local preview or redaction mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
