## Description:

Photo Cinematic Editor helps agents process photos with Pillow and NumPy, including cinematic color grading, dehazing, exposure and color adjustments, light effects, vignette, film grain, and HEIC/JPEG/PNG handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akira362680164](https://clawhub.ai/user/akira362680164)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide local photo enhancement workflows and run image-processing scripts for cinematic grading, dehazing, saturation or vibrance adjustment, levels correction, sharpening, blur, and light effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command can modify the system Python environment.

Mitigation: Install dependencies in a virtual environment or other isolated Python environment, preferably with pinned dependency versions.

Risk: Auxiliary scripts include hardcoded default OpenClaw media and workspace paths.

Mitigation: Run scripts with explicit input and output paths unless those defaults are intentionally desired.

Risk: HEIC-to-JPEG conversion and image editing can alter output files and may not preserve original metadata.

Mitigation: Work on copies of source images and preserve metadata separately when metadata retention matters.

## Reference(s):

- [Photo Editing Reference](references/photo-editing-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main script processes local image inputs through ordered effects and saves edited image files; large inputs may be resized to a maximum dimension of 3840 pixels.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
