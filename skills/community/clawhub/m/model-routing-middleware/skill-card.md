## Description:

Model Routing Middleware helps AI agents select models by task type, context size, and confidence signals to manage context and reduce model spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larios613-hub](https://clawhub.ai/user/larios613-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as middleware for AI agents that need to route prompts across local and cloud model targets based on task type, context size, and confidence or escalation signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-preview logging can expose sensitive user or business content.

Mitigation: Disable prompt-preview logging or add redaction before storing or forwarding routing logs.

Risk: Routing and escalation can send requests to configured cloud models without an explicit consent step.

Mitigation: Make cloud routing and confidence escalation opt-in for sensitive workflows, and document which model providers may receive prompts.

Risk: The skill depends on configurable model keys, endpoints, and imports that must match the deployment environment.

Mitigation: Verify package imports, model-key mappings, provider endpoints, and API credentials before operational use.

## Reference(s):

- [Model Routing Integration Guide](references/integration-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/larios613-hub/skills/model-routing-middleware)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, YAML, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routing outputs include selected model metadata, think-mode flags, confidence scores, context status, and escalation recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
