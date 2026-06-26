## Description: <br>
个人记账 helps an agent record and query personal expense and income entries from Chinese text or receipt images, storing daily records in local Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzw6](https://clawhub.ai/user/jzw6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill to have an agent capture expenses and income from Chinese natural language or receipt images, save entries by day, and produce daily or monthly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt images and personal finance details may be interpreted and saved locally. <br>
Mitigation: Use the skill only for intended personal bookkeeping data and require confirmation before writing records, especially from image-only input. <br>
Risk: Image or text parsing can record an incorrect amount, category, or date. <br>
Mitigation: Review the proposed entry before relying on saved records or daily and monthly summaries. <br>


## Reference(s): <br>
- [消费分类参考](references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown files and text responses, with JSON returned by the bookkeeping script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local bills/YYYY-MM-DD.md files and can list daily records or monthly summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
