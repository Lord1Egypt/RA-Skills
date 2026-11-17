## Description:

Store secrets, long-term memory, daily logs, and anything custom in your Convex backend instead of local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[launchthatbot](https://clawhub.ai/user/launchthatbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure OpenClaw agents to persist secrets, long-term memory, daily logs, and custom Convex backend data in a user-controlled Convex project instead of local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and daily-log functions may be exposed without evident authorization checks.

Mitigation: Use only with a Convex project you control and avoid shared or public deployments until authentication and per-agent ownership enforcement are reviewed or added.

Risk: Deploy and bridge commands rely on mutable npm package resolution around Convex and mcporter tooling.

Mitigation: Pin Convex and mcporter package versions in operational setup and verify deployment auth and target selection before writing data.

Risk: Migrating local secrets centralizes those secrets in Convex environment storage.

Mitigation: Migrate secrets only after user approval, keep CONVEX_DEPLOY_KEY local, verify copied values, and remove local secrets only after explicit cleanup confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/launchthatbot/skills/launchthatbot-convex-backend)
- [Convex](https://www.convex.dev/)
- [Convex MCP server documentation](https://docs.convex.dev/ai/convex-mcp-server)
- [Convex local components documentation](https://docs.convex.dev/components/authoring#local-components)
- [LaunchThatBot](https://launchthatbot.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Convex MCP configuration, CONVEX_DEPLOY_KEY, and deployment from the skill root before memory and daily-log functions are available.]

## Skill Version(s):

1.0.3 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
