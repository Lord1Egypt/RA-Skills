## Description:

Direct OpenSCAD scripting and rendering automation for OpenClaw - create, render, and export 3D models via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vilda007](https://clawhub.ai/user/vilda007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create parametric OpenSCAD designs, render previews, and export 3D models such as STL, PNG, and SVG outputs from an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create CAD source files and render output artifacts in the workspace.

Mitigation: Review target filenames and generated OpenSCAD content before rendering or iterating.

Risk: The skill includes operating-system package installation commands for OpenSCAD.

Mitigation: Run system package installation commands only when you trust the package manager and intend to install OpenSCAD system-wide.

## Reference(s):

- [OpenSCAD website](https://openscad.org)
- [OpenSCAD user manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual)
- [OpenSCAD language reference](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language_Reference)
- [OpenSCAD cheat sheet](https://openscad.org/cheatsheet/index.html)
- [OpenSCAD tutorial](https://en.wikibooks.org/wiki/OpenSCAD_Tutorial)
- [BOSL2 library](https://github.com/BelfrySCAD/BOSL2)
- [NopSCADlib](https://github.com/nophead/NopSCADlib)
- [ClawHub skill page](https://clawhub.ai/vilda007/skills/openscad-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with OpenSCAD code blocks and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .scad design files and render STL, PNG, or SVG artifacts when OpenSCAD is installed.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
