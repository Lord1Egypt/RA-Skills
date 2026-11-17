## Description:

Mahjong AI helps an agent identify Sichuan Mahjong hands from photos or typed tile lists and provide discard, tenpai, shanten, dingque, swap-three, safety, and opponent-pattern analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sceneun1ty](https://clawhub.ai/user/sceneun1ty)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to support Sichuan Mahjong play by turning hand photos or typed tile lists into strategy guidance, including discard recommendations, tenpai waits, shanten counts, safety scoring, dingque advice, swap-three choices, and opponent discard-pattern analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hand photos may include incidental personal, location, or table-context details.

Mitigation: Crop photos to the tiles before sending them to the assistant.

Risk: Strategy guidance depends on correct tile recognition and accurate typed inputs.

Mitigation: Confirm the recognized hand, discards, and melds before relying on the analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sceneun1ty/skills/mahjong-ai)
- [Sichuan Mahjong Theory Reference](references/mahjong_theory.md)
- [Tile Visual Identification Guide](references/tile_visual_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided hand photo or typed tile list; analysis is limited to Sichuan Mahjong tile set and rules.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
