## Description:

Inspect local media, extract audio, cut clips and frames, export subtitles, and optionally transcribe speech using local models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and media users can process local audio and video files to inspect media, extract audio, create clips and frames, export subtitles, and optionally transcribe speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional speech-recognition model downloads can use disk space.

Mitigation: Enable model downloads only when wanted and allow space for retained models and transcripts.

Risk: Dependency installation carries ordinary package risks.

Mitigation: Use a dedicated environment and reviewed dependency versions.

Risk: Generated captions may need correction before distribution.

Mitigation: Review generated captions before sharing.

## Reference(s):

- [Job contract and supported inputs](references/input.md)
- [MochiLab](https://mochilab.bz)
- [ClawHub release page](https://clawhub.ai/hznetnewpower/skills/mochi-media-workbench)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, SRT/VTT subtitles]

**Output Format:** [Audio/video clips, WAV audio, JPEG frames, SRT/VTT subtitles, JSON and Markdown transcripts, manifests, and optional ZIP archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided workspace files locally; outputs include source and output SHA-256 hashes.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
