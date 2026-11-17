## Description:

Creates and orchestrates multi-agent pipelines on the iii engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build iii-based multi-agent workflows with queue handoffs, shared state, approval gates, HTTP entry points, and completion broadcasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP-triggered workflows can accept malformed or untrusted input.

Mitigation: Validate HTTP inputs before using them to enqueue agent work or update shared state.

Risk: Shared state can retain sensitive or excessive workflow data.

Mitigation: Limit what agents store in shared state and apply retention, scoping, and access controls appropriate to the deployment.

Risk: Completion events can expose workflow results to unintended listeners.

Mitigation: Control who can subscribe to pubsub completion topics and avoid broadcasting sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/iii-agentic-backend)
- [Reference implementation: agentic-backend.js](../references/agentic-backend.js)
- [Engine configuration: iii-config.yaml](../references/iii-config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose iii worker functions, queue configuration, shared-state patterns, and approval-gate logic.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
