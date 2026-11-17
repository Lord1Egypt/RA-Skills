## Description:

Turn agent perception data into music using a zero-dependency FM synthesizer written in Zig.

This skill is ready for commercial/non-commercial use.

## Publisher:

[citriac](https://clawhub.ai/user/citriac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to sonify local perception data by mapping brightness, RMS, phase, temperature, and presence signals to FM synthesis parameters and generated audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes local audio and sensor binaries and writes generated music into the local QClaw workspace.

Mitigation: Verify the provenance of ~/.local/bin/fm_compose, ~/.local/bin/sense_all, and ffmpeg before use, especially on shared or privileged systems.

Risk: Temporary audio files are written under /tmp before being moved or deleted.

Mitigation: Prefer private temporary directories or run the skill only in trusted local environments until temp-file hardening is improved.

## Reference(s):

- [FM Synthesis Algorithm](references/fm_algorithm.md)
- [Perception to Music Mapping](references/perception_mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/citriac/skills/perception-music)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to run local scripts that generate WAV or MP3 audio files from perception data.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
