## Description:

Generate structured song lyrics in various styles and themes using the MiniMax lyrics_generation API for full song creation or editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

Songwriters, creators, and agent workflows use this skill to generate or edit structured song lyrics with style tags and section markers through MiniMax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a MiniMax API key in a local configuration file.

Mitigation: Keep the key private, restrict file access, and rotate the key if the configuration is exposed.

Risk: Prompts, titles, and existing lyrics are sent to MiniMax for generation or editing.

Mitigation: Avoid submitting confidential or proprietary text unless MiniMax's data handling terms are acceptable.

## Reference(s):

- [MiniMax lyrics_generation API endpoint](https://api.minimaxi.com/v1/lyrics_generation)
- [ClawHub skill page](https://clawhub.ai/raydoomed/skills/minimax-lyrics)
- [Publisher profile](https://clawhub.ai/user/raydoomed)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON object plus human-readable lyrics text with section tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated lyrics may include song_title, style_tags, and lyrics fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
