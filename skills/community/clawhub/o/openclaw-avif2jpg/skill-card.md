## Description: <br>
Convert `.avif` images to `.jpg` using a CLI workflow for one or more input paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoway](https://clawhub.ai/user/guoway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert individual AVIF files, folders of AVIF files, or mixed file and folder inputs into local JPEG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter writes JPEG files locally and can replace existing outputs when overwrite is enabled. <br>
Mitigation: Run it only on intended image paths, use `--recursive` only when subfolders should be scanned, and use `--overwrite` only when replacing existing JPEG files is acceptable. <br>
Risk: The workflow depends on the Pillow and pillow-avif-plugin Python packages. <br>
Mitigation: Install the dependencies only in an environment where adding those packages is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoway/openclaw-avif2jpg) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JPEG files next to source files or in sibling folder output directories; reports converted files, skipped files, and failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
