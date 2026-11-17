## Description:

观众旅程设计：设计观众的情感弧线（不是故事弧线），定义观众在每个关键时间点应该感受到什么。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, story planners, and editors use this Chinese-language skill after downstream development and before IP registration to design an audience emotional journey and produce an Audience Journey Map for the planning-to-editing handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads multiple project planning documents, which may include unpublished story, character, and world-building material.

Mitigation: Run it only in workspaces where the agent is permitted to access those planning files.

Risk: The skill writes to CLAW_WORKSPACE/99-汇总/audience-journey-map.md, which could overwrite an existing Audience Journey Map.

Mitigation: Review or back up the existing file before running the skill when preserving prior planning output matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/skills/planner-audience-journey)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown document containing an audience promise, pilot audience journey, season audience journey, consistency checks, and key design decisions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an Audience Journey Map to CLAW_WORKSPACE/99-汇总/audience-journey-map.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
