## Description:

Media Inspector analyzes local audio and video files, extracts technical metadata, optionally transcribes speech with Whisper, summarizes transcript content, identifies timestamped excerpts, and exports scan or analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensu1234](https://clawhub.ai/user/chensu1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to scan local media collections, inspect individual audio or video files, and produce structured JSON, CSV, and Markdown reports. It is useful when metadata, transcript-aware summaries, and timestamped key excerpts are needed without inferring content from filenames alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Whisper installation may introduce dependency supply-chain risk.

Mitigation: Install Whisper only from a trusted source and package name, preferably pinned to a known version.

Risk: Generated reports and raw Whisper outputs can contain sensitive transcript text from local media.

Mitigation: Write reports to a private directory and delete generated transcript artifacts when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON, CSV, and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include media metadata, transcript status, transcript text, summaries, key excerpts with timestamps, and per-file scan rows.]

## Skill Version(s):

1.0.0 (source: server release metadata and CLAWHUB.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
