## Description:

Hum2Song turns a hummed or sung melody into a complete song with local audio processing, MIDI extraction, and optional AI-assisted arrangement, without uploading sensitive recordings to third-party services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert hummed or sung recordings into MIDI and generated song files with local audio-processing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can affect the user's local Python environment.

Mitigation: Install dependencies in a dedicated virtual environment or container and review or pin third-party packages before use.

Risk: Configured output paths may overwrite existing files.

Mitigation: Choose output paths deliberately and keep intermediate MIDI files only when needed.

Risk: Optional ACE-Step use adds local model downloads and additional dependencies.

Mitigation: Enable ACE-Step only after accepting the local model download and dependency requirements; use SoundFont synthesis otherwise.

## Reference(s):

- [ACE-Step Local Music Generation](references/ace-step.md)
- [Basic Pitch Reference](references/basic-pitch.md)
- [Librosa Reference](references/librosa.md)
- [Pretty MIDI Reference](references/pretty_midi.md)
- [ACE-Step GitHub](https://github.com/ace-step/ace-step)
- [Basic Pitch GitHub](https://github.com/spotify/basic-pitch)
- [Basic Pitch Paper](https://arxiv.org/abs/2203.09893)
- [Librosa Documentation](https://librosa.org/doc/latest/)
- [Pretty MIDI Documentation](https://craffel.github.io/pretty-midi/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with inline shell and Python examples plus generated audio and MIDI file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local WAV, MP3, and MIDI artifacts depending on user options.]

## Skill Version(s):

3.0.4 (source: server release metadata, skill.json, and SKILL.md technical information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
