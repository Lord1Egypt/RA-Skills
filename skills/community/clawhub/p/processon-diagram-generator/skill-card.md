## Description: <br>
ProcessOn Diagram Generator helps agents turn natural-language diagram requests and project context into editable ProcessOn diagrams with preview and edit links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilizhang](https://clawhub.ai/user/leilizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users can ask an agent to create or redraw flowcharts, business process diagrams, architecture diagrams, ER diagrams, organization charts, timelines, roadmaps, infographics, and related visualizations in ProcessOn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts and context are sent to ProcessOn cloud services. <br>
Mitigation: Use the skill only when external ProcessOn processing is acceptable for the information in the request. <br>
Risk: The skill stores reusable local authorization tokens. <br>
Mitigation: Review, revoke, or delete cached ProcessOn credentials when they are no longer needed or when switching users. <br>
Risk: The release asks agents to run npm and shell-based setup or update steps. <br>
Mitigation: Review commands before execution and use the skill only in environments where those setup steps are permitted. <br>


## Reference(s): <br>
- [ProcessOn Diagram Generator on ClawHub](https://clawhub.ai/leilizhang/skills/processon-diagram-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with command examples and ProcessOn preview/edit links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser authorization for ProcessOn and sends diagram prompts to ProcessOn cloud services.] <br>

## Skill Version(s): <br>
2.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
