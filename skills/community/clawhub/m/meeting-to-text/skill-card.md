## Description:

Creates a local speaker-separated plain text transcript from a meeting recording, speech audio, or local audio/video file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrch1](https://clawhub.ai/user/henrch1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local meeting recordings, speech audio, and audio/video files into timestamped plain text transcripts with speaker labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can unexpectedly download a remote speaker model and load a checkpoint in a way that may execute unsafe serialized content if the model source or cache is compromised.

Mitigation: Review before installing; prefer a version with verified preinstalled model files, runtime downloads disabled, and safer checkpoint loading.

## Reference(s):

- [Runtime Paths](references/runtime_paths.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/henrch1/skills/meeting-to-text)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcript file, JSON status object, and Markdown response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript includes timestamps and speaker labels; the final non-empty stdout line is the machine-readable JSON result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
