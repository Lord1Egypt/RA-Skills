## Description:

Researches OpenClaw GitHub releases and tags for the prior Asia/Shanghai day and produces structured Markdown update reports with special attention to memory-related changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxin-lixiang](https://clawhub.ai/user/liuxin-lixiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor OpenClaw releases, identify updates from the target date, and generate concise technical Markdown reports. It is especially suited for tracking memory, embeddings, LanceDB, SQLite, and context-management changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill researches public GitHub pages and can fail or miss updates if GitHub content is unavailable or blocked.

Mitigation: Review the generated report against the linked OpenClaw release or tags page before relying on it.

Risk: The default target date uses the previous day in the Asia/Shanghai timezone, which may not match every user's local reporting window.

Mitigation: Confirm the intended research date before running the skill, especially outside the Asia/Shanghai timezone.

Risk: The skill may create a local Markdown report under report_v1 for the selected date and version.

Mitigation: Review generated files before committing, publishing, or using them in downstream release processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuxin-lixiang/skills/openclaw-update-researcher)
- [OpenClaw GitHub tags](https://github.com/openclaw/openclaw/tags)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a dated local report under report_v1 when a matching OpenClaw release is found.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
