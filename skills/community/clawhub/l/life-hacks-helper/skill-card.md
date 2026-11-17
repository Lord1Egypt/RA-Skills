## Description:

日常生活家务小助手，耐心、条理清晰地解答家务相关问题和技巧。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for beginner-friendly household guidance on cleaning, laundry, basic cooking, food storage, stain removal, home organization, and simple home maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The food-storage reference includes unsafe moldy-bread advice.

Mitigation: Review and correct the food-storage reference before installation or use.

Risk: Household guidance can affect cleaning safety and food safety decisions.

Mitigation: Review safety-sensitive answers against the vetted references and avoid presenting uncertain advice as authoritative.

## Reference(s):

- [清洁剂使用指南](artifact/references/cleaning-agents.md)
- [食材储存指南](artifact/references/food-storage.md)
- [去渍指南](artifact/references/stain-removal.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with steps, notes, and practical tips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first household advice; references are loaded only when relevant to the user question.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
