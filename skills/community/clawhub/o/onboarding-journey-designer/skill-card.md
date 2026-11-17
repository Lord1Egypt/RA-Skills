## Description:

Designs customer or employee onboarding journeys with Day 1, Day 7, and Day 30 tasks, milestones, blockers, and success metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success, enablement, HR, and product teams use this skill to turn onboarding goals, core actions, and success criteria into reviewable journey drafts and execution checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script includes dormant audit and scanning modes beyond the advertised onboarding workflow.

Mitigation: Use the default structured onboarding mode unless audit behavior is intentionally needed, and review configuration before enabling alternate modes.

Risk: The --input option can inspect local files or directories and --output can create or overwrite a report file.

Mitigation: Provide explicit non-sensitive input paths, avoid broad or sensitive directories, and choose an output path intended for generated reports.

Risk: Onboarding drafts may be too generic or may include unsupported assumptions when required context is missing.

Mitigation: Review the generated draft, fill the listed missing information, and adapt milestones and metrics to the specific product, role, or customer segment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/onboarding-journey-designer)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown, with optional JSON when the local script is invoked with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured onboarding report with Day 1, Day 7, Day 30, milestones, blocker warnings, metrics, missing information, and next steps.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
