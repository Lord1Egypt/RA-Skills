## Description: <br>
Generate CSS gradient code, preview gradient combinations, and build gradient palettes using Bash and Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to create, save, preview, and export linear, radial, and conic CSS gradients for web projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved gradient names and records may retain sensitive project context in local history. <br>
Mitigation: Avoid sensitive project names and review or delete ~/.gradient/data.jsonl when history should not be retained. <br>
Risk: Export and preview commands can overwrite files at the selected output path. <br>
Mitigation: Choose output paths deliberately and review generated files before using them in a project. <br>
Risk: The skill runs a local Bash/Python helper. <br>
Mitigation: Install and run it only in environments where local script execution is acceptable. <br>


## Reference(s): <br>
- [Gradient on ClawHub](https://clawhub.ai/xueyetianya/gradient) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [CSS gradient strings, JSON metadata, formatted tables, CSS/Tailwind/SCSS exports, and self-contained HTML previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores gradient history locally in ~/.gradient/data.jsonl and can write export or preview files to user-selected paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
