## Description:

Generates a phased HubSpot implementation roadmap from a completed audit report, including prioritized cleanup tasks, dependencies, effort estimates, and automation feasibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

HubSpot administrators and CRM operations teams use this skill after a HubSpot audit to turn findings into a sequenced cleanup, enrichment, segmentation, automation, and maintenance plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated plan may recommend CRM-changing follow-up work such as deleting, suppressing, merging, or reassigning records.

Mitigation: Confirm the selected audit report, export affected records, review a dry run where available, and require explicit approval before CRM-changing actions.

Risk: HubSpot workflow and lifecycle constraints can make some automation recommendations unsafe if followed without review.

Mitigation: Manually verify workflow trigger logic, lifecycle-stage changes, rate limits, and API constraints before implementing the plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/hubspot-implementation-plan)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown implementation plan saved as reports/implementation-plan-{YYYY-MM-DD}.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes phased tasks, dependencies, effort estimates, a tracking checklist, and HubSpot technical constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
