## Description:

A Chinese-language Guandan assistant that helps players track cards, analyze hands, suggest moves, run simulated practice games, and review learning progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External Guandan players and learners use this skill for in-game card tracking, hand analysis, move suggestions, AI practice rounds, post-game review, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Move advice, scoring, and simulations may be unreliable because the inspected implementation has simplified validation and known crash-prone paths.

Mitigation: Use the skill as a training aid and review suggested moves, scores, and simulated outcomes before relying on them during play.

Risk: Local progress tracking can persist gameplay history and learning metrics.

Mitigation: Review the local data files and avoid storing sensitive gameplay notes or personal information in progress records.

## Reference(s):

- [Guandan Rules](references/guandan_rules.md)
- [Strategy Guide](references/strategy_guide.md)
- [Card Combinations](references/card_combinations.md)
- [AI Personalities](references/ai_personalities.md)
- [Scoring Rubric](references/scoring_rubric.md)
- [Learning Path](references/learning_path.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown reports, structured text suggestions, and optional Python helper code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local game history and learning-progress data when the helper scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
