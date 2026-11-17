## Description:

Read policies, application requirements, and forms, then turn them into a completeness checklist, risk list, and submission plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to turn policy or application materials into actionable submission checklists, risk lists, timelines, and evidence trackers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided policy, application, and applicant-profile details may include sensitive information.

Mitigation: Only provide materials needed for the task and review outputs before relying on them.

Risk: Generated checklists and timelines may omit context or misread ambiguous requirements.

Mitigation: Treat outputs as planning drafts and verify requirements, deadlines, and evidence against the source materials.

Risk: The helper script can overwrite an existing file when the same --out path is reused.

Mitigation: Use a deliberate output filename and confirm before writing over existing work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/policy-application-checker)
- [README](README.md)
- [Checklist template](resources/checklist_template.md)
- [Example prompt](examples/example-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist, risk list, submission timeline, evidence tracker, and optional generated checklist file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local helper script accepts an explicit input JSON path and output path; choosing an existing output path may overwrite that file.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
