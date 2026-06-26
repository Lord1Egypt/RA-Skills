## Description: <br>
Professional photo processing and cinematic color grading powered by Pillow and NumPy for editing, retouching, dehazing, color grading, saturation, exposure, light effects, vignette, and film grain workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akira362680164](https://clawhub.ai/user/akira362680164) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-editing agents use this skill to process local photos with cinematic color grading, dehazing, levels, vibrance, light texture, sharpening, blur, vignette, glow, and HEIC/JPEG/PNG handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can affect the system Python environment when using --break-system-packages. <br>
Mitigation: Install Pillow, NumPy, and pillow-heif in a virtual environment when possible. <br>
Risk: Running helper scripts without explicit paths can read or write unintended local paths. <br>
Mitigation: Run scripts with explicit input and output file paths and review the target output location before execution. <br>


## Reference(s): <br>
- [Photo Editing Reference](references/photo-editing-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/akira362680164/photo-cinematic) <br>
- [Publisher profile](https://clawhub.ai/user/akira362680164) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash commands and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces edited local image files when the included Python scripts are run with explicit input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
