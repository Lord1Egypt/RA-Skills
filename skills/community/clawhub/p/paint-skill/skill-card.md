## Description: <br>
Generate and save simple drawings as PNG images using Python with Pillow and Tkinter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oangogah-claw](https://clawhub.ai/user/oangogah-claw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to create simple local drawing scripts and produce PNG images such as demo scenes or custom drawings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script writes to a hardcoded local output path that may not exist or may overwrite an existing file. <br>
Mitigation: Review or change the output path before running the script, and confirm whether an existing PNG should be replaced. <br>
Risk: The skill requires local Python tooling and the Pillow dependency, with Tkinter needed for documented interactive use. <br>
Mitigation: Install dependencies in an isolated environment and run the skill only where local GUI and filesystem access are acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with Markdown usage guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes image output to a local filesystem path; the included script uses a hardcoded macOS path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
