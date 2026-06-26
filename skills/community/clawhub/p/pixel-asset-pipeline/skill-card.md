## Description: <br>
AI pixel art sprite generation and processing pipeline for Godot games that generates sprite sheets with Seedream and processes them into Godot-ready assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muxueqingze](https://clawhub.ai/user/muxueqingze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game teams use this skill to generate or process pixel-art sprite sheets and convert them into Godot-ready transparent sprite sheets and frame PNGs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local Python scripts can execute image-generation or processing code selected by command-line paths. <br>
Mitigation: Use trusted JSON configs and only pass --generator or --processor paths to scripts you already trust. <br>
Risk: Generated files are written to user-selected output directories. <br>
Mitigation: Choose output directories deliberately and review generated assets before adding them to a game project. <br>


## Reference(s): <br>
- [Sample batch configuration](references/sample_config.json) <br>
- [Pixel Asset Pipeline on ClawHub](https://clawhub.ai/muxueqingze/pixel-asset-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Godot-ready sprite sheet PNGs and optional individual transparent frame PNGs when the referenced scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
