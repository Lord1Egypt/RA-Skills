## Description:

After a lesson, this skill updates a learner's error log and course map when the user uses Chinese end-of-lesson phrases such as "更新进度", "存档", or "下课".

This skill is ready for commercial/non-commercial use.

## Publisher:

[yizhan-yao](https://clawhub.ai/user/yizhan-yao)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill to save end-of-lesson progress by updating a Markdown error log and course map, then receiving a concise progress summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Short Chinese phrases such as "存档" or "下课" could activate the skill unintentionally.

Mitigation: Ask the agent to confirm the target files and update scope before applying changes when activation phrases are brief or ambiguous.

Risk: The skill modifies Markdown learning records.

Mitigation: Review proposed changes to the error log and course map before accepting them, especially when existing file structure must be preserved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown file updates with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates disclosed learning-dashboard records and avoids outputting full file contents.]

## Skill Version(s):

1.0.0 (source: plugin.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
