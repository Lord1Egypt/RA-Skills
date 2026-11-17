## Description:

历史推演聊天游戏：20年政治生命、四维环境、突发事件、羁绊、观察者、结局。触发：玩平行历史、推演历史、我想改变历史、从XX年开始。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bulletyuan](https://clawhub.ai/user/bulletyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill to run an alternate-history roleplay game in which an agent presents historical starting points, factions, location constraints, turn outcomes, legacy choices, observer-mode updates, and endings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese-language history prompts may start the roleplay game mode.

Mitigation: Install the skill only where historical roleplay behavior is desired, and test expected trigger phrases before enabling it for general historical-analysis workflows.

Risk: The skill can persist game progress in its local data/state.json file.

Mitigation: Review or reset data/state.json before sharing, packaging, or reusing a played copy when saved game history should not be retained.

## Reference(s):

- [平行历史 - 技能主文档补充](references/skill-main-supplement.md)
- [平行历史 - 历史起点配置](references/historical-starting-points.md)
- [平行历史 - 游戏机制详解](references/game-mechanics.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted Chinese text with structured turn sections, decision options, probability summaries, relationship updates, and ending summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Political-life turn outputs are capped at 5000 Chinese characters; observer-mode outputs are shorter narrative summaries.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
