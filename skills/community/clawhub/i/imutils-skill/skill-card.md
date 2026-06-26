## Description: <br>
This skill helps agents batch-process images with rotation, resizing, translation, skeletonization, and image listing workflows built around imutils-style CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JuMeng1997](https://clawhub.ai/user/JuMeng1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and automation agents can use this skill to prepare batches of product, social media, photography, or dataset images by issuing repeatable image-processing commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted filenames or option values may be interpreted as unintended shell commands by the JavaScript wrapper scripts. <br>
Mitigation: Run the skill only on trusted folders and filenames, avoid untrusted parameters, and prefer a patched wrapper that uses spawn or execFile with argument arrays. <br>
Risk: The skill depends on an external cli-anything-imutils installation to process local image files. <br>
Mitigation: Verify the installation source and behavior of cli-anything-imutils before installing or running the skill. <br>
Risk: Batch image operations may overwrite files or remove temporary files if output paths are chosen carelessly. <br>
Mitigation: Review output directories and batch scripts before execution, and keep originals in a separate trusted folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JuMeng1997/imutils-skill) <br>
- [Publisher profile](https://clawhub.ai/user/JuMeng1997) <br>
- [PyImageSearch imutils](https://github.com/PyImageSearch/imutils) <br>
- [imutils README](https://github.com/PyImageSearch/imutils#readme) <br>
- [OpenCV documentation](https://docs.opencv.org/) <br>
- [NumPy documentation](https://numpy.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or modifies local image files through external CLI execution; output paths and batch folders should be reviewed before running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, README changelog, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
