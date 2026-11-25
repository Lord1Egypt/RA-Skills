## Description:

Find an audio file’s BPM and key from a public link, look up notes, chords, Camelot codes, and delay times for any key or tempo, and use MusicWave without an account or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isunilk](https://clawhub.ai/user/isunilk)

### License/Terms of Use:

MIT-0

## Use Case:

Music producers and listeners use the skill to analyze a publicly linked audio file for tempo and key, look up notes and chord information, and calculate tempo-based delay times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a low-likelihood external-transmission alert; the skill sends requests to MusicWave and audio analysis uses a public audio URL.

Mitigation: Only provide audio URLs you are authorized to share, and review MusicWave’s privacy policy before use.

Risk: The security review is incomplete because a referenced path was not found.

Mitigation: Resolve and inspect the missing reference before installing or relying on the skill.

## Reference(s):

- [MusicWave Music Tools documentation](https://www.musicwave.ai/integrations/music-tools)
- [MusicWave privacy policy](https://www.musicwave.ai/privacy)
- [ClawHub release](https://clawhub.ai/isunilk/skills/musicwave-music-tools)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text summaries or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio analysis can include BPM, key, Camelot code, energy, danceability, and loudness.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
