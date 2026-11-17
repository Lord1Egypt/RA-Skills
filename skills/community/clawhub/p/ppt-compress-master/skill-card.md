## Description:

Compresses embedded videos and large images in PowerPoint (.pptx) files, then repackages the presentation as a valid compressed .pptx file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsingcode](https://clawhub.ai/user/tsingcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reduce PowerPoint file size for sharing by compressing embedded videos and large images while preserving a usable .pptx output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and run ffmpeg executables from external sources when bundled binaries are missing.

Mitigation: Use a trusted preinstalled ffmpeg or independently verify downloaded binaries before use.

Risk: The compression script may install Pillow during normal use.

Mitigation: Preinstall Pillow from trusted package channels in the target environment.

Risk: Generated Python commands may include user-provided file paths.

Mitigation: Use only trusted .pptx files, validate the path before execution, and avoid unusual filenames or untrusted message text in commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsingcode/skills/ppt-compress-master)
- [Publisher Profile](https://clawhub.ai/user/tsingcode)
- [FFmpeg Windows Build Source](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
- [FFmpeg macOS ffmpeg Build Source](https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip)
- [FFmpeg macOS ffprobe Build Source](https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip)
- [FFmpeg Linux Static Build Source](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands; local execution can produce a compressed .pptx file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports original size, compressed size, compression ratio, and output file path when compression runs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
