## Description: <br>
Store secrets, long-term memory, daily logs, and anything custom in your Convex backend instead of local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[launchthatbot](https://clawhub.ai/user/launchthatbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to persist agent secrets, long-term memory, daily logs, and custom Convex backend data in their own Convex project instead of local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write sensitive secrets and agent memory in a Convex project. <br>
Mitigation: Use it only with an intended Convex deployment, keep CONVEX_DEPLOY_KEY local and private, and verify the target deployment before secret or memory writes. <br>
Risk: Migrating local .env keys could move credentials into a shared backend used by multiple agents. <br>
Mitigation: Review the keys selected for migration, exclude CONVEX_DEPLOY_KEY and CONVEX_DEPLOYMENT, verify copied keys, and remove local secrets only after explicit cleanup approval. <br>
Risk: Agents sharing one Convex project may share memories, logs, or credentials more broadly than intended. <br>
Mitigation: Use a dedicated Convex project when agents should not share state, and follow the documented per-agent secret naming convention for scoped overrides. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/launchthatbot/launchthatbot-convex-backend) <br>
- [LaunchThatBot publisher profile](https://clawhub.ai/user/launchthatbot) <br>
- [Convex](https://www.convex.dev/) <br>
- [Convex MCP server documentation](https://docs.convex.dev/ai/convex-mcp-server) <br>
- [Convex local components documentation](https://docs.convex.dev/components/authoring#local-components) <br>
- [LaunchThatBot website](https://launchthatbot.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operational guidance for Convex MCP setup, secret handling, memory persistence, daily logs, and Convex backend customization.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
