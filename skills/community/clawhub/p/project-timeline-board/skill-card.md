## Description:

A data-driven project timeline board that lets users edit a JavaScript configuration file to generate an HTML page with an intelligent timeline, Gantt chart, milestone tracking, and to-do board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ildar981105-create](https://clawhub.ai/user/ildar981105-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and project teams use this skill to create a configurable project planning page for milestones, schedules, task status, and delivery coordination. It is suited to product planning, release scheduling, design handoff, and project progress updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured timeline text and extras content may be treated as page markup.

Mitigation: Use trusted project configuration only, or sanitize/rewrite renderer fields to use textContent or explicit DOM creation before hosting on a sensitive origin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ildar981105-create/skills/project-timeline-board)
- [Timeline CSS component reference](references/timeline-css.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a static project timeline template driven by PROJECT_CONFIG data.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
