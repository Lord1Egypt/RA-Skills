## Description:

Converts `.avif` images to `.jpg` using a CLI workflow for one or more file or folder paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoway](https://clawhub.ai/user/guoway)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to convert AVIF images into JPEG files from individual paths or batches of files and folders. It is useful when image assets need broader JPG compatibility while keeping outputs beside the source location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes JPG files next to source AVIF files or in a sibling output directory, which may create files in user-selected filesystem locations.

Mitigation: Review input paths before running the command and confirm that the expected adjacent or sibling output location is acceptable.

Risk: Using `--overwrite` can replace existing JPG outputs.

Mitigation: Use `--overwrite` only when replacing prior JPG outputs is intended.

Risk: The documented dependency installation command does not pin package versions.

Mitigation: Install dependencies in a virtual environment or another isolated environment before running the converter.

## Reference(s):

- [OpenClaw AVIF to JPG on ClawHub](https://clawhub.ai/guoway/skills/openclaw-avif2jpg)
- [Publisher profile: guoway](https://clawhub.ai/user/guoway)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates JPG files next to individual AVIF inputs or under a sibling '<folder>_jpg' directory for folder inputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
