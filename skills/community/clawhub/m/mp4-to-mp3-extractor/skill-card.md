## Description:

Batch extracts audio from .mp4 files in a chosen directory into .mp3 files while preserving the source folder structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local folders of MP4 videos into MP3 audio files, optionally choosing an output folder or letting the skill create a default sibling folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a user-selected video folder and writes MP3 outputs.

Mitigation: Run it only on intended local folders and review the output directory before processing large or sensitive collections.

Risk: The skill changes Python package state and uses a shared virtual environment.

Mitigation: Prefer a private, pinned virtual environment and review dependency changes before installation.

Risk: The skill may download and run FFmpeg automatically.

Mitigation: Prefer preinstalled FFmpeg from a trusted source and verify the executable path before running conversions.

Risk: The documented sudo symlink workaround can affect system-wide Python command resolution.

Mitigation: Avoid the workaround unless an administrator has reviewed the command and confirmed the host-level impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/mp4-to-mp3-extractor)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves relative folder structure and writes conversion logs in the skill logs directory.]

## Skill Version(s):

1.1.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
