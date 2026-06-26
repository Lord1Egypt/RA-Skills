## Description: <br>
Builds and maintains a knowledge graph for long-term memory with concept drift detection and temporal reasoning. Use when storing structured knowledge, detecting concept changes over time, or performing temporal queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to store structured long-term memory as concepts and relationships, query related knowledge, detect concept changes over time, and perform temporal reasoning over recorded events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security result is low confidence because the supplied scan summary says the target skill artifact was not available for a full artifact-backed review. <br>
Mitigation: Confirm the visible instructions and code match the intended behavior before installing, and reject deployments that request unnecessary credentials, broad filesystem access, or automatic background execution. <br>
Risk: Long-term memory can retain outdated, incorrect, or sensitive information if callers store it without review. <br>
Mitigation: Review stored concepts and events, apply retention rules for sensitive data, and validate memory-derived answers before using them in user-facing or automated decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-knowledge-graph-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Code, JSON, Guidance] <br>
**Output Format:** [JavaScript API responses, serialized JSON graph data, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces in-process knowledge graph, concept drift, temporal event, and memory management outputs; no external credentials were detected in the supplied evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
