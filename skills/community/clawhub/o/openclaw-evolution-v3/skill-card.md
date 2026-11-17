## Description:

Guides OpenClaw users through safe upgrades from executor-style agents to coordinator-style agents with mandatory synthesis, partitioned task scheduling, context checks, and proof-driven verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacurtwong](https://clawhub.ai/user/jacurtwong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to assess compatibility, plan incremental policy updates, apply Gene Locking templates, and verify coordinator-mode behavior before rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent OpenClaw agent-policy upgrades that affect agent behavior.

Mitigation: Use a dedicated branch or rollback point, review exact diffs to IDENTITY.md and AGENTS.md, apply changes incrementally, and run local verification before promotion.

Risk: Automatic collection of environment variables can expose secrets.

Mitigation: Do not allow environment-variable values to be read unless there is a specific need and secrets are redacted or allowlisted.

Risk: Applying coordinator-mode templates without compatibility checks can conflict with existing permission and orchestration policies.

Mitigation: Confirm target structure and policy files first, preserve the existing permission pipeline, and verify ask/allow behavior after each change.

## Reference(s):

- [Compatibility & Safety Guardrails](references/COMPATIBILITY.md)
- [OpenClaw Agent v3.0: Evolution Guide from Assistant to Coordinator](references/EVOLUTION_GUIDE_EN.md)
- [OpenClaw Agent v3.0: Evolution Guide Chinese](references/EVOLUTION_GUIDE_CN.md)
- [OpenClaw Evolution v3 Coordinator Upgrade Blueprint](references/README_REPO_EN.md)
- [OpenClaw Evolution v3 Coordinator Upgrade Blueprint Chinese](references/README_REPO_CN.md)
- [SOP: Gene Locking for v3.0 Coordinator](references/SOP_GENE_LOCKING.md)
- [ClawHub Skill Page](https://clawhub.ai/jacurtwong/skills/openclaw-evolution-v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, code snippets, and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scope, risks, exact edits, validation commands, and rollback planning when executing an evolution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
