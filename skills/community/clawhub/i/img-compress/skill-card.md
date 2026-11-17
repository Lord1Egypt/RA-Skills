## Description:

Batch compresses JPG and PNG image files to reduce file size while keeping image dimensions unchanged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginntech](https://clawhub.ai/user/ginntech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to compress batches of JPG and PNG assets when images are too large or need optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad in-place overwrites can alter or damage original image assets.

Mitigation: Run only on backed-up copies or a staging directory before applying changes to important assets.

Risk: The documented examples use sudo and include web server asset paths.

Mitigation: Run as an unprivileged user and avoid production or system-owned paths unless the target directory has been separately constrained.

Risk: The skill depends on Pillow being installed in the Python environment.

Mitigation: Pin and install Pillow in an isolated environment before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a Python/Pillow script that overwrites matching image files in place.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
