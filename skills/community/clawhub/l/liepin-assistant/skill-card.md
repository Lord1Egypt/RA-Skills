## Description:

猎聘求职助手封装 Liepin MCP 服务，帮助用户搜索职位、查看 JD、投递简历和管理简历。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyapersonal](https://clawhub.ai/user/wangyapersonal)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to interact with Liepin through an agent: configure a Liepin token, search job listings, inspect job details, submit applications after review, and view or update resume information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Liepin account token that can expose resume data and authorize account actions while valid.

Mitigation: Set LIEPIN_TOKEN through a secure environment or secret manager, do not paste real tokens into chat, and revoke or rotate tokens when no longer needed.

Risk: The fallback config.json path can store credentials in plaintext.

Mitigation: Prefer the environment variable path and avoid writing tokens to config.json unless the storage location is reviewed and protected.

Risk: Resume edits and job applications can change user account state.

Mitigation: Require explicit user review and confirmation before any resume update or job application.

## Reference(s):

- [Liepin MCP API Reference](references/api.md)
- [Liepin MCP Credential Page](https://www.liepin.com/mcp/server)
- [Liepin MCP Endpoint](https://open-agent.liepin.com/mcp/user)
- [ClawHub Skill Page](https://clawhub.ai/wangyapersonal/skills/liepin-assistant)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Liepin token for authenticated job search, application, and resume actions.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
