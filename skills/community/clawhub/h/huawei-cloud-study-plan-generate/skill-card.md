## Description:

Generates configurable study practice plans with topic rotation, non-overlapping daily sessions, and reproducible output when seeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and developers use the skill to create a structured study schedule with topics, practical exercises, and session durations. They can adjust the plan and choose Markdown, plain text, or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing to an existing output path overwrites its contents.

Mitigation: Choose a new output path or check the destination before running with --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-study-plan-generate)
- [Usage Guide](references/usage-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Verification Method](references/verification-method.md)
- [Data Flow](references/dataflow-diagram.md)
- [IAM Policies](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON]

**Output Format:** [Markdown table, plain text, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A fixed seed makes the generated plan reproducible.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
