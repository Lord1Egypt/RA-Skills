## Description:

Jiuge Flow Perfect V1 guides an agent through a local audio-processing workflow that separates vocals, applies de-reverb processing, and produces 48 kHz master and preview MP3 files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzgsrbs](https://clawhub.ai/user/lzgsrbs)

### License/Terms of Use:

MIT-0

## Use Case:

Audio creators and automation agents use this skill to run a repeatable local vocal separation, optional wash, de-reverb, and MP3 mastering pipeline for prepared input recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can operate outside the intended input and output folders when given a path-like filename.

Mitigation: Use only simple filenames already placed in Jiuge_Input and prefer a fixed version that rejects path separators and traversal before creating output directories or running cleanup.

Risk: Audio files may contain sensitive recordings when processed on shared systems.

Mitigation: Avoid sensitive recordings on shared systems and review local storage locations before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzgsrbs/skills/jiuge-base-behavior)
- [SKILL.md](artifact/SKILL.md)
- [jiuge_flow.sh](artifact/scripts/jiuge_flow.sh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled shell workflow creates project folders and audio files when executed in a prepared local environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
