## Description: <br>
Project Timeline Board helps agents generate a configurable project timeline page from a JavaScript project configuration, including key nodes, a Gantt chart, milestones, and a to-do board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ildar981105-create](https://clawhub.ai/user/ildar981105-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and project planners use this skill to create a data-driven timeline board by editing project dates, milestones, Gantt rows, and task lists in configuration rather than hand-editing HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed PROJECT_CONFIG files may contain embedded HTML or script-like payloads that run in the rendered page. <br>
Mitigation: Install only from trusted sources, review shared configuration files before opening them, and prefer versions that render fields as text or sanitize allowed markup. <br>


## Reference(s): <br>
- [Timeline CSS reference](references/timeline-css.md) <br>
- [ClawHub skill page](https://clawhub.ai/ildar981105-create/project-timeline-board) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML and JavaScript configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local page assets and configuration-oriented instructions for rendering a project timeline board.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
