## Description: <br>
Structured free-thinking and exploration for agents that lets them choose or accept a topic, journal what they learn, and track follow-up action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mculp](https://clawhub.ai/user/mculp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their users use Open Thoughts to reserve idle or requested time for curiosity-driven research, reflection, journaling, and follow-up tracking. It supports manual, heartbeat, or isolated cron invocation while keeping cron exploration private. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exploration journals are durable local workspace memory and may preserve sensitive topics, personal details, or contact information. <br>
Mitigation: Review or delete files under explorations periodically, and avoid sensitive topics or raw contact details unless they are necessary. <br>
Risk: Callback requests create saved action items that could later be used to contact a person or agent. <br>
Mitigation: Require user review before any saved action item is used to send a message or otherwise contact someone. <br>
Risk: Generic triggers or scheduled invocations can start explorations when the user did not intend to create persistent notes. <br>
Mitigation: Narrow broad triggers when the host supports it, and enable scheduled use only when durable exploration notes are desired. <br>


## Reference(s): <br>
- [Open Thoughts examples](artifact/references/examples.md) <br>
- [Open Thoughts on ClawHub](https://clawhub.ai/mculp/open-thoughts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown journal entries and action-item lists written to workspace files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends files under explorations; callback requests become action items for later reviewed follow-up.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
