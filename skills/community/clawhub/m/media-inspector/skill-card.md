## Description: <br>
Local audio and video analysis tool that scans media files, extracts metadata, optionally transcribes speech with Whisper, generates summaries, and identifies timestamped key excerpts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensu1234](https://clawhub.ai/user/chensu1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and media operators use this skill to inventory local audio and video files, inspect metadata, and generate per-file reports with optional transcript-based summaries and timestamped excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain private local paths, metadata, summaries, excerpts, and full transcript text. <br>
Mitigation: Store reports in a private location, restrict access to output directories, and delete or protect reports after analyzing sensitive recordings. <br>
Risk: The skill depends on local ffmpeg and optional Whisper tooling to inspect or transcribe media. <br>
Mitigation: Install ffmpeg and Whisper only from trusted sources and run the skill on specific files or narrow folders. <br>


## Reference(s): <br>
- [Media Inspector on ClawHub](https://clawhub.ai/chensu1234/media-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, CSV, and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include local file paths, media metadata, transcript text, summaries, and timestamped excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: CLAWHUB.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
