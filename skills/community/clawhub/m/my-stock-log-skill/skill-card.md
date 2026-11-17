## Description:

This skill archives and retrieves U.S. stock analysis conclusions in a fixed DingTalk multidimensional table when explicitly invoked by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record validated U.S. stock analysis conclusions and query prior analysis records from the configured DingTalk table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append stock-analysis conclusions to and read records from a specific DingTalk Base and Sheet when explicitly invoked.

Mitigation: Before installation or use, confirm the fixed DingTalk destination is intended and that the dingtalk-ai-table integration has only the access needed for that table.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-log-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables for query results and structured text guidance for validated insert operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Insert summaries are constrained to 300 characters by the skill instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
