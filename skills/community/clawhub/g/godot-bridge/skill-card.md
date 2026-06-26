## Description: <br>
Godot Bridge is a Godot 4.x project generator CLI that helps agents create 2D and 3D project scaffolds, scenes, scripts, UI, game components, assets, and export presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scaffold Godot 4.x games, add scenes, scripts, UI, gameplay systems, assets, and export presets during rapid prototyping or automated game-development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates as a local project-generation CLI that writes files in the user's workspace. <br>
Mitigation: Use it in a dedicated Godot project folder and review generated files before running or committing them. <br>
Risk: The security evidence reports that the local Godot launcher is implemented unsafely and should be reviewed before installation. <br>
Mitigation: Avoid or carefully review `clawbridge open` until it launches Godot without shell parsing. <br>
Risk: Project and file names are used to create local paths and generated content. <br>
Mitigation: Avoid path separators and shell metacharacters in project, scene, script, and file names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/godot-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/dashiming) <br>
- [Godot Engine](https://godotengine.org) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated Godot project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes Godot project files in the current workspace when commands are executed.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
