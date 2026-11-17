## Description:

Media Processor helps agents work with audio and video through format conversion, editing, transcription, extraction, and batch-oriented media processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations teams use this skill to guide or generate local Python and FFmpeg-based workflows for transcoding, clipping, merging, watermarking, audio processing, speech transcription, and subtitle or text output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media operations can overwrite user-selected output files.

Mitigation: Run the skill in a restricted workspace, review every input and output path before processing, avoid shared writable directories, and keep backups of source media.

Risk: Video merge behavior uses an unsafe fixed temporary filename.

Mitigation: Run merge operations in an isolated working directory, avoid concurrent merges in the same directory, and update the implementation to use unique temporary files before production use.

Risk: Installation guidance includes optional sudo-based FFmpeg package installation commands.

Mitigation: Treat system package installation as an administrative step and run it only after confirming the package source and environment policy.

Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin and audit dependencies before production deployment and install them in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/media-processor)
- [Project homepage](https://github.com/openclaw/media-processor)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, media processing options, dependency notes, and generated transcript or subtitle file guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
