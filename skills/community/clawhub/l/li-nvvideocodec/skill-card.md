## Description:

Compresses batches of video files with FFmpeg using NVIDIA NVENC AV1 hardware encoding, with compression-profile selection and validation before full runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check FFmpeg and NVIDIA GPU readiness, analyze folders of video files, and run AV1 batch compression through test or full-compression workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended batch compression can consume significant GPU, CPU, disk, and time resources, especially when an agent invokes non-interactive mode.

Mitigation: Use explicit input and output folders, start with test mode and a small test count, and require user review before full compression.

Risk: The compression script can attempt to install the tqdm dependency automatically if it is missing.

Mitigation: Install pinned dependencies in an isolated environment before running the skill and review dependency sources before allowing execution.

Risk: Already-compressed videos may become larger or lose quality if compressed again.

Mitigation: Use the built-in validation pass first and stop when the validation report indicates compression is not worthwhile.

## Reference(s):

- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with shell commands, plus JSON status for environment checks and video analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compression actions write processed video files to a separate output directory and report progress and summary text.]

## Skill Version(s):

1.0.1 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
