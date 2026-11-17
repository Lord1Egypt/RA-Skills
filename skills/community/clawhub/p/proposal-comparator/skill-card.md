## Description:

Compares multiple proposal documents and produces differences, hidden costs, risks, and recommendations for decision workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and decision teams use this skill to compare proposals for reviews, procurement decisions, or technical selection. It produces an auditable Markdown draft that separates facts from inferred recommendations and calls out missing information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposal inputs can include sensitive commercial or personal information.

Mitigation: Process only local files the user is comfortable sharing with the agent, and redact sensitive details before use when needed.

Risk: The skill may write a report to a user-selected output path when the local script is run.

Mitigation: Review the output path before execution or use dry-run/stdout behavior when a persistent file is not needed.

Risk: Generated recommendations may overstate conclusions when source proposals lack evidence or constraints.

Mitigation: Keep facts separate from inferred advice, preserve missing-information sections, and review recommendations before making decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/proposal-comparator)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Example Output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown or JSON report generated from local input files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language structured comparison report with sections for comparison dimensions, pros and cons, hidden costs, risks, recommendations, reservations, and follow-up items.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
