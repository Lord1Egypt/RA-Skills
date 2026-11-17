## Description:

Godot 4.x Project Generator CLI for creating 2D and 3D Godot projects, scenes, scripts, levels, UI, game components, physics elements, particles, animations, materials, and export presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to generate and modify Godot 4.x game project files for rapid prototyping and automated game-development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security review flags unsafe file-path handling that can make generated writes risky in normal development workspaces.

Mitigation: Use the skill only in a disposable or explicitly approved workspace, and avoid untrusted project paths or generation arguments.

Risk: The authoritative security review flags unsafe shell-command handling for opening Godot from project directories.

Mitigation: Do not run `clawbridge open` from untrusted directories until shell invocation and path validation are fixed.

Risk: The release security verdict is suspicious, even though no exfiltration or hidden persistence was found.

Mitigation: Review the skill before installation and scan generated files before moving them into a trusted project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dashiming/skills/godot-bridge)
- [Publisher Profile](https://clawhub.ai/user/dashiming)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands and generated Godot project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and writes project, scene, script, asset, level, UI, and export configuration files in the active workspace.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
