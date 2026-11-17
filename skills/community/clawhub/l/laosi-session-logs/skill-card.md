## Description:

会话日志分析 - 搜索和分析历史会话日志，查找之前的对话内容和结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect recent local session logs, search prior conversations, extract key information, and filter results by time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive local session history and may expose private conversation content or secrets in returned snippets.

Mitigation: Require explicit user approval before log searches and redact secrets or sensitive values before presenting results.

Risk: The sample behavior can read more history or files than users would reasonably expect.

Mitigation: Enforce date limits, restrict searches to known log files, reject traversal and absolute paths, and limit result counts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-session-logs)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown summaries with optional Python code examples, tables, and search-result lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should be scoped, limited, and redacted before returning session-log snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
