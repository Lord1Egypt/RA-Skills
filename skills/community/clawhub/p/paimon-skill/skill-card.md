## Description:

派蒙.skill lets an OpenClaw agent inspect Genshin Impact screenshots, answer gameplay questions, and optionally perform simple UI actions such as clicks, key presses, and button lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgandgameenginelearner](https://clawhub.ai/user/cgandgameenginelearner)

### License/Terms of Use:

MIT-0

## Use Case:

External players and agent users use this skill with OpenClaw for Genshin Impact guidance, screen analysis, and supervised UI assistance when they are stuck on tasks, menus, combat, exploration, or character development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture and save screenshots, and click_text can send screenshots to Alibaba Cloud/DashScope.

Mitigation: Use it only with non-sensitive windows visible, keep notifications hidden, and limit use to game sessions where cloud image processing is acceptable.

Risk: The skill can control mouse and keyboard input, including a global click fallback when the target window is not found.

Mitigation: Run click_text with --dry-run first, supervise execution, and stop use if the target game window is not clearly active and scoped.

Risk: The skill can store an API key in a local config file.

Mitigation: Prefer the DASHSCOPE_API_KEY environment variable over saved keys, use a restricted key where possible, and rotate the key after testing.

Risk: The dependency list uses minimum versions rather than pinned exact versions.

Mitigation: Install in an isolated Python environment and review or pin dependencies before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cgandgameenginelearner/skills/paimon-skill)
- [BetterGI click implementation analysis](references/better-gi-click-analysis.md)
- [Game automation pattern reference](references/game-patterns.md)
- [Alibaba Cloud GUI-Plus API documentation](https://bailian.console.aliyun.com/cn-beijing?tab=api#/api/?type=model&url=2997660)
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [JSON command results, screenshot file paths, shell commands, and agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may save local screenshots and may return post-action screenshot paths for feedback loops.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
