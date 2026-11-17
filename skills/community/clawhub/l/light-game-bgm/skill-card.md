## Description:

Composes original light, melodic, loopable background music for cozy game town, village, and overworld themes and renders it into playable audio using MIDI, soundfonts, expressive performance, reverb, and loop verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzwu2017](https://clawhub.ai/user/yzwu2017)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, composers, and game makers use this skill to create original loopable background music for light game scenes and deliver playable audio with supporting MIDI and editable composition code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs third-party audio tools and Python packages.

Mitigation: Install only reviewed tools and prefer pinned or reviewed dependency versions.

Risk: Downloaded soundfont files may be untrusted, redirected, or invalid.

Mitigation: Use trusted sources, verify downloaded soundfonts with SHA-256 hashes when possible, and confirm the file is a real SoundFont before loading it in FluidSynth.

Risk: Generated loops may have audible seams or clipping if shipped without verification.

Mitigation: Run the bundled loop verification step and review seam and peak results before delivery.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yzwu2017/skills/light-game-bgm)
- [Soundfonts, instruments & rendering reference](artifact/references/soundfonts.md)
- [GeneralUser GS soundfont download](https://www.dropbox.com/s/4x27l49kxcwamp5/GeneralUser_GS_v1.471.sf2?dl=1)
- [FluidR3 GM soundfont release](https://github.com/fhunleth/midi_synth/releases/download/v0.1.0/FluidR3_GM.sf2)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Audio files]

**Output Format:** [Markdown guidance with Python and bash code blocks plus generated MP3, MIDI, WAV, and Python composition files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Loopable music assets should be verified for seam continuity and clipping before delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
