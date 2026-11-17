## Description:

Liaomei Skill is a social coaching skill that helps users record dating interactions, review outcomes, practice low-pressure conversations, and track progress while rejecting manipulative tactics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wnzzer](https://clawhub.ai/user/wnzzer)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a social-growth coach for recording invitations, icebreakers, conversations, reviews, mood interventions, and progress statistics. It is intended for respectful dating practice and personal reflection, not manipulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores intimate relationship interactions and mood notes in long-lived local files.

Mitigation: Choose a storage directory under user control, avoid real names or contact details, and regularly review or delete saved files and backups.

Risk: The skill uses shell-based write instructions for local records.

Mitigation: Review proposed file operations before execution and prefer safer write patterns with explicit confirmation for sensitive records.

Risk: Error handling may echo raw sensitive records when a write fails.

Mitigation: Redact sensitive details before sharing errors and add purge or redaction controls before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wnzzer/skills/liaomei-skill)
- [Analytics Reference](references/analytics.md)
- [Field Guide](references/field-guide.md)
- [Mindset Reference](references/mindset.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured records and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON and JSONL memory files for user profiles, invitations, interactions, conversations, and reviews.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
