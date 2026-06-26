## Description: <br>
Direct OpenSCAD scripting and rendering automation for OpenClaw - create, render, and export 3D models via CLI <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vilda007](https://clawhub.ai/user/vilda007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and engineers use this skill to create, modify, preview, and export parametric OpenSCAD models through an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation, modification, and rendering of local CAD output files, including .scad, .stl, .png, and .svg files. <br>
Mitigation: Use a dedicated project folder and require confirmation before modifying or overwriting existing CAD or render output files. <br>
Risk: OpenSCAD must be installed locally before render commands can work. <br>
Mitigation: Verify the openscad binary is installed and available before asking the agent to render or export models. <br>


## Reference(s): <br>
- [OpenSCAD](https://openscad.org) <br>
- [OpenSCAD User Manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual) <br>
- [OpenSCAD Language Reference](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language_Reference) <br>
- [OpenSCAD Cheat Sheet](https://openscad.org/cheatsheet/index.html) <br>
- [OpenSCAD Tutorial](https://en.wikibooks.org/wiki/OpenSCAD_Tutorial) <br>
- [BOSL2](https://github.com/BelfrySCAD/BOSL2) <br>
- [NopSCADlib](https://github.com/nophead/NopSCADlib) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with OpenSCAD code examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or rendering of local .scad, .stl, .png, and .svg files through the OpenSCAD CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
