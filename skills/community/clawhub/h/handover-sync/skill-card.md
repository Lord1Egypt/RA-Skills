## Description:

Summarize end-of-session development progress and sync project handoff documentation in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loo-y](https://clawhub.ai/user/loo-y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill at the end of a development session to inspect repository evidence, summarize actual changes, and keep handoff documentation aligned for the next teammate or agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow may update README sections and nearby handoff notes in addition to handover.md.

Mitigation: Clarify the allowed document scope before use and review the resulting diff before accepting changes.

Risk: A handoff can mislead future work if it summarizes from memory or omits unverified checks.

Mitigation: Ground the handoff in repository evidence, name validations actually performed, and explicitly label anything not verified.

## Reference(s):

- [Chinese Session Summary Template](artifact/references/session_summary_template.md)
- [English Session Summary Template](artifact/references/session_summary_template.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown handoff documentation and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update handover.md, README.md, and nearby TODO or runbook notes when the user does not narrow scope.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
