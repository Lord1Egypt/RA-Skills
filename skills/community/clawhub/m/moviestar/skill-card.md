## Description:

Edit and verify videos with the MovieStar CLI, including trimming, multicamera composition, captions, audio mixing, and rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdilla1277](https://clawhub.ai/user/jdilla1277)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and other users can guide an agent to inspect, edit, render, and verify local video and audio with MovieStar and FFmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editing operations may overwrite generated outputs or project state.

Mitigation: Use a dedicated task directory, review dry-runs, and confirm replacements before applying them.

Risk: Installing dependencies or downloading transcription models can change the local environment.

Mitigation: Use a virtual environment and obtain approval before package installation or model downloads.

Risk: A successful render may still contain visual or audio errors.

Mitigation: Inspect representative frames and audio, probe the export, and report unresolved warnings.

## Reference(s):

- [MovieStar homepage](https://trymoviestar.com)
- [MovieStar on ClawHub](https://clawhub.ai/jdilla1277/skills/moviestar)
- [Editing workflows](artifact/references/editing-workflows.md)
- [Installation guidance](artifact/references/installation.md)
- [Render verification](artifact/references/verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text with CLI commands and output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports editing choices, media properties, and unresolved warnings.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
