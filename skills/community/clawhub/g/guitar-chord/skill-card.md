## Description:

Guitar Chord helps agents look up guitar chord notes, identify chords from notes, show inversions and drop2 voicings, and return scale information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deantiwang](https://clawhub.ai/user/deantiwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask an agent for guitar chord, scale, inversion, and drop2 voicing guidance. It is useful for lightweight music-theory lookup and command-oriented chord analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional diagram feature may build and run a local Cargo project from ~/workspace/ascii_chord.

Mitigation: Use non-diagram chord and scale features by default, and enable --diagram only after reviewing and trusting the local ascii_chord project.

Risk: Some advertised behavior may be incomplete or unreliable, including capo calculation and reverse lookup.

Mitigation: Validate important chord, scale, and capo outputs against a trusted music-theory source before using them in lessons, publications, or performance material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deantiwang/skills/guitar-chord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chord note lists, ASCII diagrams, scale diagrams, inversion lists, and drop2 voicing tables.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
