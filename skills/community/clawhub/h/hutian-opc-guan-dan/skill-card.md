## Description: <br>
掼蛋AI助手：手牌识别、记牌、出牌建议、虚拟对局、陪练模式、复盘系统。当用户需要打掼蛋辅助、识别手牌、记牌、出牌建议、练习提升或复盘学习时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Guandan players use this skill for live card tracking, move suggestions, AI practice games, observation mode, and post-game review. The skill supports learning through scoring, mistake analysis, progress tracking, and rule-reference guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store local Guandan learning progress, game history, and mistake statistics. <br>
Mitigation: Use explicit Guandan-related prompts to avoid accidental activation, and clear local progress data on shared machines or when practice history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/hutian-opc-guan-dan) <br>
- [Guandan rules](references/guandan_rules.md) <br>
- [Strategy guide](references/strategy_guide.md) <br>
- [Card combinations](references/card_combinations.md) <br>
- [AI personalities](references/ai_personalities.md) <br>
- [Scoring rubric](references/scoring_rubric.md) <br>
- [Learning path](references/learning_path.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured game-state, hand-report, move-suggestion, review, and progress templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local JSON progress and game-history files during practice and review workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
