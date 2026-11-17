## Description:

Track everything about your home, appliances, service history, contractors, and upcoming maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to maintain a conversational home record across appliances, service history, contractors, costs, warranties, and maintenance reminders for one or more properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves household records locally, including addresses, appliance details, contractor contact information, warranty dates, service notes, and repair costs.

Mitigation: Share only details you are comfortable storing on the device, and review or delete home-data.json when household records change or the machine is shared.

Risk: Maintenance reminders and cost summaries depend on the completeness and accuracy of stored user-provided records.

Mitigation: Review logged entries after updates, correct missing dates or costs, and treat reminders as planning aids rather than professional inspection or safety advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris/skills/home-maintenance-os)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown responses with structured JSON records persisted locally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local home-data.json record for properties, appliances, service history, contractors, schedules, warranties, notes, and costs.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
