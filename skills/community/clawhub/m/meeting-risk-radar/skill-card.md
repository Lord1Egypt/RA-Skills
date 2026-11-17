## Description:

Identifies high-risk topics, unclear responsibilities, missing materials, and potentially disruptive discussion points before meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, facilitators, and team leads use this skill to prepare for meetings by turning a meeting topic, attendees, and expected decisions into a reviewable risk brief with missing materials, unclear ownership, agenda changes, confirmation questions, and contingency plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled dormant audit and pattern-scanning modes can inspect local directories and files if enabled.

Mitigation: Install and run the skill only in workspaces where broader local inspection is acceptable, and review script arguments before enabling directory or pattern audit modes.

Risk: Meeting materials may contain private or sensitive information.

Mitigation: Use redacted inputs where possible and keep outputs as reviewable drafts before sharing or acting on them.

Risk: The brief may miss context or produce incomplete risk judgments when meeting inputs are sparse.

Mitigation: Require explicit confirmation of missing materials, unclear responsibilities, and listed unknowns before using the brief for facilitation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/meeting-risk-radar)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Structured output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown risk brief, with optional JSON output from the bundled local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local script accepts an input file, directory, or inline text and can write to stdout or an output file; normal skill use produces reviewable drafts rather than external system changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
