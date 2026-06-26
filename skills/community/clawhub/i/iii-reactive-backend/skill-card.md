## Description: <br>
Builds reactive real-time backends on the iii engine for event-driven apps where state changes trigger side effects, clients receive live updates via streams or websockets, or teams need a real-time database layer with pub/sub and CRUD endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design iii engine backends where CRUD state changes drive reactive side effects, aggregate metrics, and live client updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CRUD endpoints, state triggers, or live streams could expose or mutate application data if scopes and authorization are too broad. <br>
Mitigation: Review generated backend code before deployment, verify authorization and stream scoping, and keep reactive handlers focused on intended state changes. <br>
Risk: State triggers fire on any change in a scope, which can create unintended side effects or expensive work. <br>
Mitigation: Use event fields such as new_value, old_value, and key to filter relevant changes, and offload heavy work to queues or background processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rohitg00/iii-reactive-backend) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with code-oriented implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on iii state triggers, CRUD endpoints, streams, and pattern boundaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
