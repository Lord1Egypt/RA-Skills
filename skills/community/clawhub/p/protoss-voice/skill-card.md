## Description:

Apply Protoss-style (StarCraft) psionic effects to ANY audio file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vemec](https://clawhub.ai/user/vemec)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to post-process existing TTS output or user-provided recordings into a Protoss-style voice effect. It transforms audio files with SoX and FFmpeg and writes a processed output file alongside the input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary audio artifacts may be silently deleted, and predictable temporary paths can be overwritten in shared directories.

Mitigation: Run the skill in a private working directory, check for existing _psionic outputs or hidden temporary files with the same base name, and avoid processing recordings that must be preserved without backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vemec/skills/protoss-voice)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a processed audio file with a _psionic suffix; requires ffmpeg and sox.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
