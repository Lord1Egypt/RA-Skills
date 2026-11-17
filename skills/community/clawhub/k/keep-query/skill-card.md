## Description:

Queries a user's Keep App exercise records, body measurements, health metrics, daily statistics, recent data, and historical trends through the Keep MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuchuanhao1](https://clawhub.ai/user/liuchuanhao1)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill through an Agent Skills or MCP-capable agent to retrieve and display their own Keep App exercise, body, and health data. It is intended for data lookup and presentation, not for health analysis, medical advice, or unsupported statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Keep account credentials in a local ~/.keepai/.env file.

Mitigation: Install only on trusted machines, avoid shared environments, and revoke or clear the token when finished.

Risk: The package runs install-time code that can modify OpenClaw or Hermes skill directories and send install telemetry.

Mitigation: Review install behavior before deployment and install only if the @keepclaw package source and target runner directories are trusted.

Risk: The package depends on an unpinned @keepclaw/skill-sdk dependency.

Mitigation: Pin and review dependency versions in controlled deployments before installing or updating the skill.

Risk: The skill can access personal health and activity data through the Keep MCP endpoint.

Mitigation: Use it only for authorized user data queries and do not treat returned data as medical advice.

## Reference(s):

- [ClawHub Keep 数据查询 Skill Page](https://clawhub.ai/liuchuanhao1/skills/keep-query)
- [Keep MCP Gateway](https://mcp.gotokeep.com/skills-mcp-gateway-page/v1)
- [Keep QR Login Authentication Guide](references/auth.md)
- [Keep Query Tool Guide](references/query.md)
- [Keep Revoke Auth Guide](references/revoke-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON MCP call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents upstream Keep query results without inventing missing data, unsupported statistics, or health advice.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
