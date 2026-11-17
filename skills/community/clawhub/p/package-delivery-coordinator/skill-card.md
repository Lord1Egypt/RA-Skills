## Description:

Coordinate several expected deliveries using a user-provided watchlist, conflict check, follow-up plan, and message templates for neighbors or front desk staff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to coordinate multiple expected package deliveries from details they provide, including delivery windows, helper availability, building constraints, and package risks. It produces a watchlist, conflict-aware action plan, copy-ready messages, follow-up checkpoints, and a retrieval checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted messages may include package, address-type, name/unit, schedule, or helper details.

Mitigation: Review messages before sending and omit pickup codes, account links, private tracking links, or unnecessary personal information.

Risk: The skill does not independently verify carrier or delivery status.

Mitigation: Use only user-provided tracking status and arrival windows, mark missing details as unknown, and ask the user to supply updated information when needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables, checklists, and message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output based on user-provided delivery details; no carrier, account, calendar, location, camera, weather, or building-system access.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
