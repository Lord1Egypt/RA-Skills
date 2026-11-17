## Description:

Problem Mapper helps agents turn ambiguous decisions or strategic questions into structured problem maps with definitions, success criteria, risk assessment, and candidate action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to analyze complex decisions, product planning questions, interview scenarios, and strategy problems before committing to an execution plan. It supports both guided multi-turn analysis and one-pass Markdown problem-map reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash, Read, and Write permissions even though the documented workflow is primarily prompt-driven problem analysis.

Mitigation: Review requested permissions before installation, avoid granting shell access unless explicitly needed, and limit any export or write behavior to user-approved files.

Risk: The workflow can produce persuasive strategic or decision guidance that may be incomplete without domain context.

Mitigation: Treat outputs as structured analysis aids, verify assumptions and metrics with relevant stakeholders, and use qualified experts for high-impact legal, financial, compliance, or operational decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/problem-mapper)
- [Five Clarifying Questions](artifact/references/five-clarifying-questions.md)
- [Risk Mapping Guide](artifact/references/risk-mapping.md)
- [Problem Map Template](artifact/templates/problem-map-template.md)
- [Dialogue Mode Prompt Template](artifact/templates/dialogue-prompt.md)
- [Waterfall Mode Prompt Template](artifact/templates/waterfall-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, structured tables, guided questions, and action-plan outlines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce long-form problem maps of roughly 3000-5000 Chinese characters in waterfall mode, or staged dialogue summaries in multi-turn mode.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
