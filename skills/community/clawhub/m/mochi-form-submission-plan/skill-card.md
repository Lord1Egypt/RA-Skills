## Description:

Map requested values to an observed form, identify missing required fields and separate review from final submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People and agents preparing a form review use this skill to compare supplied values with observed form fields, identify missing or unknown fields, and produce a review plan before any live action. It checks data locally and does not fill or submit forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form requests can contain personal or sensitive values.

Mitigation: Include only data needed for review and remove sensitive request files when finished.

Risk: A local review result does not establish that a live submission is accurate or authorized.

Mitigation: Inspect the report before any live submission and follow host approval requirements for purchases, agreements, or account changes.

## Reference(s):

- [Input contract](references/input.md)
- [Chinese usage guidance](references/zh-CN.md)
- [Publisher website](https://mochilab.bz)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-form-submission-plan)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON review report and task-specific local artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports readiness, missing and unknown field names, sensitive field names, and whether submission occurred; does not include field values.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
