## Description:

法索 AI 法律助手，提供法律条文检索功能。当用户询问法律问题、查询法规条文、查找司法解释、了解法律条款内容时自动触发。包括：查询特定法律（如劳动法、合同法、民法典）、根据案件情况检索相关法律依据、了解某个法律概念的具体规定等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daixin877889](https://clawhub.ai/user/daixin877889)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal-domain practitioners use this skill to search legal provisions, regulations, and judicial interpretations through the LexSeek API. The agent analyzes case facts, extracts professional legal keywords, runs authenticated searches, and presents cited results with a reminder to consult a qualified lawyer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests LexSeek phone-number and password credentials through chat or command arguments.

Mitigation: Prefer scoped tokens or browser/OAuth-style login and do not provide reusable passwords in chat or CLI arguments.

Risk: The skill stores a LexSeek API key locally in the skill directory.

Mitigation: Store credentials in a managed secret store or protected environment variables instead of the skill directory.

Risk: The skill sends legal queries to LexSeek and depends on an external API for results.

Mitigation: Install only when LexSeek data sharing is acceptable, pin the API URL to the legitimate LexSeek host, and handle API failures without adding unsupported legal answers.

Risk: The release includes obfuscated network code.

Mitigation: Review or replace the obfuscated script before deployment and confirm it only contacts expected LexSeek endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daixin877889/skills/lexseek)
- [LexSeek registration and service site](https://lexseek.cn)
- [登录与认证](artifact/references/auth.md)
- [法律 API 接口](artifact/references/legal-api.md)
- [LexSeek API base URL](https://api.lexseek.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with cited legal provisions and inline shell commands for LexSeek authentication and search]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LexSeek authentication and should not supplement missing search results with model knowledge.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
