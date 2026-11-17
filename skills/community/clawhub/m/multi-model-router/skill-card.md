## Description:

Automatically routes tasks to a suitable local or cloud AI model based on privacy, context length, cost, and performance requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keven0706](https://clawhub.ai/user/keven0706)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate model selection across local and cloud models for long-context, privacy-sensitive, cost-sensitive, or performance-critical agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or private context may be routed to cloud models despite stated privacy protections.

Mitigation: Review before installation, require explicit consent for cloud routing of sensitive content, or change fallback behavior to fail closed to a local model.

Risk: Routing decisions rely on pattern-based privacy detection and may miss sensitive data that does not match configured patterns.

Mitigation: Treat privacy detection as advisory, review configured patterns and thresholds, and avoid sending secrets, credentials, private documents, or sensitive workspace context through automatic routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keven0706/skills/multi-model-router)
- [ClawHub publisher profile](https://clawhub.ai/user/keven0706)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON-compatible routing result with selected model, context, reason, and analysis fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also write local audit-log entries for routing decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
