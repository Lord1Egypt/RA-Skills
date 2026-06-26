## Description: <br>
Convert, compress, merge, split, clip, inspect, and extract audio locally with FFmpeg, plus decode supported music-cache formats including pure-Python Ximalaya .xm and optional Kugou/local helper formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to process local audio and video files, including conversion, compression, merging, splitting, clipping, inspection, and supported music-cache decoding. It is suited for local file workflows where FFmpeg, FFprobe, and optional helper tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional split cleanup flag can recursively delete the selected output directory. <br>
Mitigation: Use a new empty output directory for split jobs and avoid --clean on any folder containing important files. <br>
Risk: The skill runs FFmpeg and optional locally configured helper programs. <br>
Mitigation: Install and configure only trusted helper binaries, and run diagnose before processing files. <br>


## Reference(s): <br>
- [Core Behavior Reference](references/core-behavior.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces local file-processing guidance and may return JSON containing input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
