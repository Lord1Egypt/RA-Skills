## Description:

OpenRA-RL lets an AI agent play Command & Conquer: Red Alert by using MCP tools to observe the battlefield, manage production, command units, and advance game time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxc20089](https://clawhub.ai/user/yxc20089)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an AI agent to an OpenRA Red Alert environment, configure the MCP server, and guide RTS gameplay through observation, production, movement, combat, and planning tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external Python package and Docker image.

Mitigation: Review the linked project, pin a known package version, and check which Docker image is pulled before running the server.

Risk: The game server starts a local service for agent interaction.

Mitigation: Keep the server bound to local access unless you intentionally expose it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxc20089/skills/openra-rl)
- [OpenRA-RL GitHub Repository](https://github.com/yxc20089/OpenRA-RL)
- [OpenRA-RL PyPI Package](https://pypi.org/project/openra-rl/)
- [OpenRA-Bench Leaderboard](https://huggingface.co/spaces/yxc20089/OpenRA-Bench)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, MCP tool calls]

**Output Format:** [Markdown with tables, inline code, JSON configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent through iterative game-state observation, command issuance, and time advancement.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
