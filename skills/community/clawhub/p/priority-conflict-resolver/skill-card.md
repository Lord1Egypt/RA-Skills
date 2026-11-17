## Description:

Helps resolve priority conflicts across multiple goals and constrained resources by producing task ordering, trade-off rationale, boundaries, review points, and a not-to-do list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn goal lists, resource constraints, and conflict descriptions into a review-first priority plan for scheduling conflicts, limited resources, and scope control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script can read user-selected files or directories and can write to a user-selected output path.

Mitigation: Provide only intended input paths, choose output paths carefully, and use dry-run or stdout output when reviewing behavior.

Risk: The skill ships dormant local audit modes that could broaden file inspection if the bundled configuration is changed.

Mitigation: Review future changes to artifact/resources/spec.json before running artifact/scripts/run.py.

Risk: Priority recommendations may be incomplete or misleading when inputs omit goals, constraints, or conflicts.

Mitigation: Treat outputs as review drafts, confirm missing information, and keep final priority decisions under human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/priority-conflict-resolver)
- [README](artifact/README.md)
- [Structured configuration](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Example output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown by default, with optional JSON from the local Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-first output with task ordering, rationale, trade-offs, communication wording, review points, re-evaluation triggers, and missing-information prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
