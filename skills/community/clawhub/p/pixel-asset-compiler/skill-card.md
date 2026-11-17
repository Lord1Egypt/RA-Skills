## Description:

Compile AI-generated pixel character references and separately named action sheets into deterministic, validated game assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn AI-generated sprite references and action sheets into deterministic, audited, game-ready asset packages and Godot 4 AnimatedSprite2D exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run the pixel-asset-compiler CLI from npm if no local executable is available.

Mitigation: Prefer an already installed or project-local reviewed CLI; when npm installation is required, pin and verify the trusted package version and avoid elevated privileges.

Risk: Incorrect sprite semantics or failed quality gates can produce unusable animation assets.

Mitigation: Require explicit manifest semantics, stop on ambiguity, preserve passed actions, regenerate only failed actions, and rerun inspect, compile, audit, validate, and export before reporting success.

## Reference(s):

- [Manifest v1](references/manifest-v1.md)
- [Quality Gates](references/quality-gates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON manifest guidance, and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow reports, generic asset packages, and Godot export files when the referenced CLI is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
