## Description:

Creates original MIDI instrumental compositions, melodies, chord progressions, ambient loops, game music, and website music from user-provided titles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lostviolinist](https://clawhub.ai/user/lostviolinist)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a title or short creative brief into a generated MIDI instrumental artifact with a manifest, composition plan, critic score, and optional audio preview. It supports candidate selection, blind audition rating, and local preference learning for future compositions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save local music-preference history, including optional feedback notes, under the user's home directory.

Mitigation: Avoid entering sensitive personal information in feedback unless it is intended to be stored, and delete ~/.hermes/music-composer-preferences.json to reset the learned taste profile.

## Reference(s):

- [Composer Protocol](references/composer-protocol.md)
- [Song Recipes](references/song-recipes.json)
- [Project Homepage](https://github.com/lostviolinist/music-composer-skill)
- [ClawHub Skill Page](https://clawhub.ai/lostviolinist/skills/midi-music-composer)
- [Publisher Profile](https://clawhub.ai/user/lostviolinist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated file paths for MIDI, JSON manifests, composition plans, and optional WAV audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local MIDI and JSON artifacts; optional audio rendering depends on local timidity or fluidsynth availability.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
