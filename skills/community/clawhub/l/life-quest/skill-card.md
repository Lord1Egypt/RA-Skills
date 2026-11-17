## Description:

人生游戏的任务指引系统。将人生比作没有保存/载入功能的RPG游戏，帮助用户管理人生主线任务和支线任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaopanguo](https://clawhub.ai/user/shaopanguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language skill to frame life planning as an RPG quest system, set or revisit a main life goal, rank daily side quests by relevance and urgency, and get direction when they feel uncertain about what to do next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad phrases about feeling lost or uncertain.

Mitigation: Review activation behavior and treat its output as general life-planning guidance rather than professional counseling or crisis support.

Risk: The skill is designed to store a local profile and main quest in its references.

Mitigation: Review, edit, or clear the local user-profile reference if persistent personal goal notes are not desired.

## Reference(s):

- [Life Quest Skill Page](https://clawhub.ai/shaopanguo/skills/life-quest)
- [Motivation Library](references/motivation-library.md)
- [Quest Templates](references/quest-templates.md)
- [User Profile](references/user-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown-style task rankings and short planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized task lists, relevance and urgency labels, main-quest reminders, and brief encouragement.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
