## Description:

Hot Video Breakdown downloads a user-provided short-video link, transcribes it locally with faster-whisper, lets the calling AI analyze the transcript, and generates an interactive capsule-card HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content teams use this skill to turn an explicitly provided short-video URL into a local transcript, structured AI analysis, and an interactive HTML breakdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-provided video URLs and may read a user-supplied cookie file.

Mitigation: Run it only on trusted public video URLs, avoid cookies unless necessary, and confirm the source, title, and duration before transcription.

Risk: The skill downloads a Whisper model and writes transcript, analysis, and report files locally.

Mitigation: Use a controlled working directory, review generated files before sharing, and avoid processing private or sensitive videos.

Risk: Generated HTML from untrusted analysis JSON is identified by security evidence as unsafe until inspected.

Mitigation: Inspect or sanitize analysis JSON and generated HTML before opening it, especially when the analysis JSON came from an untrusted source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouq2039-lang/skills/hot-video-breakdown)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhouq2039-lang)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, guidance]

**Output Format:** [JSON status objects, transcript text files, analysis JSON, and interactive HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally after dependencies are installed; writes transcript, analysis, and report files under the configured output directory.]

## Skill Version(s):

1.0.2 (source: frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
