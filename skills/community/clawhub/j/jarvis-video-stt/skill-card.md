## Description:

Jarvis-Video-STT helps agents batch-transcribe video files with Faster-Whisper and produce subtitles, plain-text transcripts, and summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and automation agents use this skill to convert batches of MP4, MKV, AVI, or MOV videos into SRT subtitles, text transcripts, and processing reports for review or content preprocessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted video filenames may trigger unintended shell command execution during audio extraction.

Mitigation: Review before installing or running; process only trusted filenames and directories, and prefer a fixed version that invokes ffmpeg through subprocess.run with an argument list and shell=False.

Risk: Transcripts and reports may contain sensitive spoken content.

Mitigation: Choose an appropriate output directory, restrict access to generated SRT, TXT, JSON, and Markdown files, and review retention requirements before processing sensitive media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chongjie-ran/skills/jarvis-video-stt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with command-line examples and generated SRT, TXT, JSON, and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive spoken content written to the selected output directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
