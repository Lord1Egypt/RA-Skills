## Description:

调用 JavaSkillController 提供的 HTTP 接口，供 OpenClaw/OpenLaw 执行业务操作、健康检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintqiu](https://clawhub.ai/user/lintqiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call trusted JavaSkillController HTTP endpoints for OpenClaw/OpenLaw business operations, data queries, submissions, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user and business data to a user-configured Java backend over HTTP endpoints.

Mitigation: Install only when you control and trust JAVA_API_URL; prefer HTTPS except for local development and avoid sending sensitive data unless the backend and transport are protected.

Risk: Broad triggers and submit-style actions may perform state-changing operations.

Mitigation: Require explicit user confirmation before submit or other state-changing actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, JSON]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JAVA_API_URL to point to a trusted backend; supports execute, execute-v2, and health endpoints.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
