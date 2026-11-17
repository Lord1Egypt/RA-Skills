## Description:

Triage user-feedback issues in Linear, especially FB team / 用户反馈 workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwqcode](https://clawhub.ai/user/qwqcode)

### License/Terms of Use:

MIT-0

## Use Case:

Support and product teams use this skill to query Linear feedback issues, classify complaints, identify duplicates, recommend labels and statuses, and draft concise user replies for the Tide feedback process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs an unpinned npm command that may execute changing third-party package code.

Mitigation: Pin or preinstall mcporter from a trusted source before using the skill.

Risk: The workflow can read and modify Linear business tickets.

Mitigation: Use least-privilege Linear credentials and require clear user confirmation before any write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwqcode/skills/linear-feedback-triage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional inline shell commands and reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include issue IDs, statuses, labels, duplicate recommendations, grouping buckets, and proposed Linear write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
