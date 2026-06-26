## Description: <br>
Applies event-driven async messaging to decouple producers and consumers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architects use this skill for guidance on when and how to apply event-driven architecture, including event modeling, broker selection, failure handling, observability, and operational deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad architecture triggers may surface this skill for tasks that are not specifically about event-driven design. <br>
Mitigation: Confirm the task involves asynchronous messaging, pub/sub, brokers, event streams, or loose coupling before applying its recommendations. <br>
Risk: Event-driven systems can create hidden coupling through undocumented event semantics or fields. <br>
Mitigation: Maintain an event catalog or schema registry and validate event contracts before implementation. <br>
Risk: Asynchronous pipelines can be difficult to diagnose when failures or stuck consumers are not observable. <br>
Mitigation: Define dead-letter queues, retries, idempotency, tracing, and operational dashboards as part of the architecture review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-archetypes-architecture-paradigm-event-driven) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown prose, checklists, and architecture recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no tools, commands, API keys, or runtime dependencies detected.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
