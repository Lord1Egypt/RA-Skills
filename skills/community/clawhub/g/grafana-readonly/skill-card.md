## Description: <br>
Read existing Grafana dashboards and panels without modifying them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwqcode](https://clawhub.ai/user/qwqcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analytics users use this skill to locate Grafana dashboards and panels, inspect panel queries and variables, and rerun existing panel-backed queries under different time ranges or variable selections without modifying Grafana assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may answer from the wrong Grafana dashboard or panel when search results are ambiguous. <br>
Mitigation: The skill directs the agent to inspect dashboard structure, panels, variables, and assumptions before answering confidently. <br>
Risk: A user may request dashboard creation, updates, deletions, alerts, or annotations outside the read-only scope. <br>
Mitigation: The skill explicitly prohibits create, update, and delete actions and directs the agent to hand off to a build-oriented workflow when modification is required. <br>
Risk: Existing panels or variables may not support the requested split, filter, or analysis question. <br>
Mitigation: The skill directs the agent to state variable and time-range assumptions and escalate when no matching dashboard, panel, or variable exists. <br>


## Reference(s): <br>
- [Grafana Readonly release page](https://clawhub.ai/qwqcode/grafana-readonly) <br>
- [Grafana Readonly Action Checklist](references/action-checklist.md) <br>
- [Grafana Skill Evaluation Notes](references/evaluation-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, API calls] <br>
**Output Format:** [Markdown or plain text with summarized Grafana findings and referenced dashboard, panel, variable, and time-range assumptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Grafana workflow guidance; raw Grafana JSON is avoided unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
