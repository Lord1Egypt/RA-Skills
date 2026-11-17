## Description:

Add, remove, or rename OpenClaw model IDs by reconciling provider catalogs, policy, fallbacks, and per-agent references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate OpenClaw model catalog entries while keeping provider catalogs, model policy, defaults, fallbacks, and per-agent references consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model registry, policy, default, fallback, or per-agent changes can affect future OpenClaw agent behavior.

Mitigation: Review the proposed diff before applying it and verify parsing, schema validation, effective model availability, and reload logs after the change.

Risk: Removing or renaming a model ID before replacing dependent primary or fallback references can leave stale or broken configuration.

Mitigation: Audit registry, policy, defaults, fallbacks, aliases, runtime metadata, and every per-agent reference before applying one atomic patch.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed diffs, validation steps, shell commands, and configuration changes when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose an atomic configuration patch or an exact human-applied diff when no authorized writer is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
