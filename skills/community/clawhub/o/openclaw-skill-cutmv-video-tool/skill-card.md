## Description:

A video processing skill for OpenClaw that uses FFmpeg to cut, convert, compress, inspect, annotate, and extract media files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT License

## Use Case:

Developers and agent builders use this skill to automate common media-processing tasks such as trimming clips, converting formats, compressing video for messaging limits, extracting frames or audio, and adding watermarks or subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports unsafe evaluated FFprobe output and a suspicious verdict.

Mitigation: Install only from a trusted publisher, run in a constrained workspace, avoid attacker-supplied media, and replace evaluated parsing with strict numeric parsing before broad deployment.

Risk: Security evidence reports output overwrite behavior without clear safeguards.

Mitigation: Use dedicated media input and output directories, review output paths before execution, and require explicit overwrite control in production workflows.

Risk: Subtitle paths, watermark values, style values, and output paths are processed through FFmpeg filters.

Mitigation: Validate and escape media-related inputs before use, especially when values come from untrusted users or automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaotucodes/skills/openclaw-skill-cutmv-video-tool)
- [Publisher profile](https://clawhub.ai/user/qiaotucodes)
- [FFmpeg](https://ffmpeg.org/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python API examples, CLI commands, and generated media or metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg in PATH; processing can overwrite output files when invoked with existing paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
