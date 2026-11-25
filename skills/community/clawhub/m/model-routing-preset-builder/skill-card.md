## Description:

Use when the operator asks to create or change a native model-routing policy for Codex or OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create or change native model-routing policies for Codex or OpenClaw. It helps preserve existing selections and validate model and effort availability for the target runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two unresolved references leave some scanner evidence incomplete.

Mitigation: Review the referenced router material and verify model and effort availability in the target runtime before applying a policy.

## Reference(s):

- [Bundled pstack role presets](references/pstack-role-presets.json)
- [Canonical Codex pstack role presets](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/references/pstack-role-presets.json)
- [Canonical OpenClaw subscription guidance](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/references/openclaw-subscriptions.md)
- [Canonical model capability router instructions](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown, Shell commands]

**Output Format:** [Markdown with model-routing recommendations and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime-specific recommendations with validation evidence and remaining availability gaps.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
