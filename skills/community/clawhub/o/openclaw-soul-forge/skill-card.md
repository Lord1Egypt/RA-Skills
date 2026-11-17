## Description:

Forge a complete lobster soul for an OpenClaw AI Agent, including identity positioning, SOUL.md, character-driven boundary rules, a name, and an avatar prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to design or randomize characterful lobster personas and produce SOUL.md, IDENTITY.md, boundary rules, names, and avatar prompts for OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOUL.md and IDENTITY.md may overwrite files if generated in a directory that already contains those filenames.

Mitigation: Use a dedicated output directory and review the target path before confirming file writes.

Risk: Optional avatar generation depends on baoyu-image-gen, which is outside the core skill.

Mitigation: Use the manual avatar prompt fallback unless baoyu-image-gen has been separately reviewed.

Risk: A highly characterful generated persona can become too restrictive for normal agent tasks.

Mitigation: Apply the included intensity calibration and reforge or trim the persona if it constrains useful behavior.

## Reference(s):

- [OpenClaw Persona Forge Homepage](https://github.com/eamanc-lab/openclaw-persona-forge)
- [Avatar Style & Image Generation](references/avatar-style.md)
- [Boundary Rules](references/boundary-rules.md)
- [Error Handling & Degradation Strategy](references/error-handling.md)
- [Identity Tension](references/identity-tension.md)
- [Naming System](references/naming-system.md)
- [Full Output Template](references/output-template.md)
- [Optional baoyu-image-gen Skill](https://github.com/JimLiu/baoyu-skills)
- [Adam Avatar Style Reference](https://raw.githubusercontent.com/eamanc-lab/openclaw-persona-forge/main/docs/adam-claw-logo.png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown with optional SOUL.md and IDENTITY.md file outputs, shell command snippets, and avatar prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The core output is text; avatar image generation is optional and falls back to a reusable prompt when the optional dependency is unavailable.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
