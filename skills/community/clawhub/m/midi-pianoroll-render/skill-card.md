## Description:

Use when a MIDI file needs rendering as a piano roll image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, musicians, educators, and external users use this skill to render MIDI files as vertical Synthesia-style or horizontal DAW-style piano-roll PNG images for reading, teaching, sharing, or inspecting song structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted or unusually large MIDI files may create ordinary local resource-use risk.

Mitigation: Run the renderer only on trusted MIDI files or inside a resource-limited environment.

Risk: Saving the rendered PNG to an existing output path can replace that file.

Mitigation: Choose output paths deliberately and avoid pointing the renderer at files that should be preserved.

Risk: Unpinned local dependencies can reduce reproducibility across environments.

Mitigation: Install dependencies in a virtual environment and pin versions when reproducible output matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flobo3/skills/midi-pianoroll-render)
- [Publisher profile](https://clawhub.ai/user/flobo3)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG files with Markdown guidance and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vertical or horizontal piano-roll images from local MIDI inputs; rendering options include bar count, start bar, melody track, and accompaniment track.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
