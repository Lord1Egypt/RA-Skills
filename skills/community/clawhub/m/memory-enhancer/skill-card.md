## Description:

Automatically extracts facts from daily logs to update and maintain structured long-term memory and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpneuma](https://clawhub.ai/user/xpneuma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-knowledge users use this skill to automatically extract preferences, contacts, habits, and project status from daily memory logs into long-term memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily logs may contain private, sensitive, regulated, or third-party information that is sent to an external model for analysis.

Mitigation: Use only with logs appropriate for external analysis, or require a local-only or redacted processing path before deployment.

Risk: The spawned agent can write long-term memory entries without human review.

Mitigation: Prefer an opt-in workflow with preview-before-write and schema validation for memory updates.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON file updates, Markdown summary entries, and status/log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes daily memory logs and writes merged memory statistics plus concise summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
