## Description: <br>
Generate Rhino 7 Grasshopper (.ghx) XML files from natural language descriptions or images, using native Grasshopper components, GhPython scripts, and graph wiring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elliotbian](https://clawhub.ai/user/elliotbian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational designers, and architects use this skill to generate Rhino 7 Grasshopper definitions for parametric forms such as towers, facades, Voronoi patterns, diagrids, surfaces, meshes, and custom Python geometry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .ghx output can overwrite existing project files if saved to an unintended path. <br>
Mitigation: Save generated files to a deliberate project or temporary folder and avoid reusing existing filenames unless replacement is intended. <br>
Risk: Generated GhPython components may contain geometry logic that should not be run blindly inside Rhino or Grasshopper. <br>
Mitigation: Review generated GhPython code and plugin dependencies before opening or executing the definition in Rhino/Grasshopper. <br>


## Reference(s): <br>
- [Grasshopper Generator README](README.md) <br>
- [Grasshopper Component GUID Database](references/component_guids.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/elliotbian/grasshopper-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and generated .ghx XML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated .ghx files are intended for Rhino 7 Grasshopper and may include native component wiring or GhPython fallback code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
