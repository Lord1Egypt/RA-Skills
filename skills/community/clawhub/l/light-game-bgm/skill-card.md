## Description: <br>
Composes light, melodic, loopable background music for cozy game themes and helps render it into playable audio using MIDI, soundfonts, expressive performance, reverb, and loop verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzwu2017](https://clawhub.ai/user/yzwu2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and creators use this skill to create original loopable BGM for games, prototypes, or soundtrack experiments, including MIDI composition, sampled-instrument rendering, reverb processing, and loop quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install local audio tools or Python packages and may download soundfonts from external sites. <br>
Mitigation: Install only the listed dependencies you trust, validate downloaded soundfonts before use, and keep package and soundfont sources under normal project review. <br>
Risk: The skill creates local MIDI, WAV, MP3, and Python files whose paths and generated content may need review before use. <br>
Mitigation: Review generated output paths, inspect editable scripts, and run the bundled loop verification before shipping or relying on rendered audio. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yzwu2017/light-game-bgm) <br>
- [Soundfonts, instruments, and rendering reference](references/soundfonts.md) <br>
- [FluidR3_GM soundfont release](https://github.com/fhunleth/midi_synth/releases/download/v0.1.0/FluidR3_GM.sf2) <br>
- [GeneralUser GS soundfont download](https://www.dropbox.com/s/4x27l49kxcwamp5/GeneralUser_GS_v1.471.sf2?dl=1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash and Python snippets; generated artifacts may include MP3, WAV, MIDI, and Python files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, FluidSynth, FFmpeg, mido, numpy, and scipy; metadata indicates macOS and Linux support.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
