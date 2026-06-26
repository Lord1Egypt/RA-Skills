## Description: <br>
Run local ComfyUI workflows via the HTTP API, including default or user-supplied workflow JSON, model-weight downloads, and generated image delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to edit and run local ComfyUI workflow JSON through the ComfyUI HTTP API, download model weights into a local ComfyUI install, and return generated images to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download pget and model weights from external URLs and place files into a local ComfyUI installation. <br>
Mitigation: Use trusted sources, known hashes or checksums when available, and prefer --no-pget or a separately installed trusted pget. <br>
Risk: The bundled temporary workflow contains a prefilled adult prompt and should not be treated as a safe default workflow. <br>
Mitigation: Review and edit workflow JSON before running; prefer the default workflow or a user-approved workflow. <br>
Risk: Running workflows depends on a local ComfyUI server and model files, which may execute user-provided graph behavior through ComfyUI. <br>
Mitigation: Run only reviewed workflows in a controlled local environment and confirm server availability before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-image) <br>
- [ComfyUI project](https://github.com/comfyanonymous/ComfyUI.git) <br>
- [pget project](https://github.com/replicate/pget) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON workflow edits, and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ComfyUI server, Python 3, and trusted model-weight sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
