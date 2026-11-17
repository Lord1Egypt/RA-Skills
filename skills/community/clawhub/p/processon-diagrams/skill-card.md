## Description:

This deprecated compatibility alias tells agents that `processon-diagrams` has been renamed to `processon-diagramgen` and should no longer be used as the primary ProcessOn diagram workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halloweb](https://clawhub.ai/user/halloweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this alias to preserve backward compatibility when older prompts or workflows mention `processon-diagrams`. The skill guides the agent to notify users about the rename and continue with `processon-diagramgen` instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect this alias to perform the full diagram generation workflow.

Mitigation: Tell users that `processon-diagrams` is deprecated and continue with the separate `processon-diagramgen` skill.

Risk: The behavior of actual diagram generation is outside this compatibility alias.

Mitigation: Review and trust the separate `processon-diagramgen` skill before relying on redirected diagram generation behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halloweb/skills/processon-diagrams)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deprecated alias guidance only; actual diagram generation behavior is delegated to the separate `processon-diagramgen` skill.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
