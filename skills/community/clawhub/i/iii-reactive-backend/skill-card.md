## Description:

Builds reactive real-time backends on the iii engine for event-driven apps where state changes trigger side effects, clients receive live updates via streams or websockets, or a real-time database layer with pub/sub and CRUD endpoints is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design iii reactive backends with state-triggered side effects, CRUD state access, live stream or websocket updates, and aggregate metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated backend code may expose state scopes, delete endpoints, or public stream/websocket surfaces in ways that affect application data and network access.

Mitigation: Review generated backend code before deployment, with specific attention to state scope boundaries, destructive endpoints, and stream or websocket exposure.

Risk: Reactive triggers can unintentionally propagate side effects when any value in a watched state scope changes.

Mitigation: Use event fields such as new_value, old_value, and key to filter trigger behavior and keep reactive handlers focused and fast.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/iii-reactive-backend)
- [ClawHub publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no bundled execution behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
