## Description:

Use when the user asks for learning goals, capability development, reflection, teaching, replication, transfer readiness, or applying a PBL loop in a real project context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlxeva](https://clawhub.ai/user/dlxeva)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run capability-learning loops in real project work, separating delivery evidence from capability evidence across start, checkpoint, and transfer modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional persistence could retain learning notes beyond a single conversation.

Mitigation: Enable persistence only with explicit user approval and store only user-approved notes in a user-selected project-local location.

Risk: Learning-loop outputs could overstate user capability if delivery evidence is treated as capability evidence.

Mitigation: Keep delivery evidence and capability evidence separate, require evidence status on claims, and fail closed when repeatability or transfer evidence is missing.

## Reference(s):

- [Server-resolved source import](https://github.com/dlxeva/pbl-loop/tree/main/pbl-loop)
- [FlowGrid optional companion](https://github.com/dlxeva/FlowGrid)
- [PBL Loop trigger and boundary tests](references/trigger-boundary-tests.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured JSON-like fields for start, checkpoint, and transfer responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation-only by default; optional project-local notes only when the user explicitly authorizes persistence.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
