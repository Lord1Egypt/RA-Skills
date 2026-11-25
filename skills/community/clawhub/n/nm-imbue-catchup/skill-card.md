## Description:

Summarizes recent git changes for context recovery after session breaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when returning to ongoing work or preparing a handoff. It summarizes changes across Git repositories, meeting notes, sprint tracking, documents, or logs, then organizes insights, follow-ups, and blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes log-analysis behavior alongside Git context summaries.

Mitigation: Confirm that log analysis fits the task, and review conclusions against the relevant source logs.

Risk: The security scan reports partial inspection of the Git-patterns file, so coverage does not establish that every part of the skill is safe.

Mitigation: Review the skill guidance before relying on its results, especially for consequential decisions.

## Reference(s):

- [Catchup skill release on ClawHub](https://clawhub.ai/athola/skills/nm-imbue-catchup)
- [Related project homepage (listed in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown with Summary, Key Changes, Follow-ups, and Blockers/Questions sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The summary is scoped to the selected Git, document, meeting, sprint, or log baseline.]

## Skill Version(s):

1.10.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
