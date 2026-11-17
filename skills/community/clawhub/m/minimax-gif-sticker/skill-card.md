## Description:

Converts photos of people, pets, objects, or logos into four captioned animated GIF stickers in a Funko Pop / Pop Mart style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daidai8910g](https://clawhub.ai/user/daidai8910g)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative-tool developers use this skill to turn a submitted photo into a small set of animated sticker GIFs with custom or language-aware captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User photos and facial likenesses may be processed by external MiniMax services.

Mitigation: Use the skill only with explicit consent from anyone depicted and only when external processing of the image is acceptable.

Risk: Referenced scripts and dependency files are not included in the artifact for review.

Mitigation: Obtain and inspect the publisher's helper files before use, including what data they transmit and how they handle credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daidai8910g/skills/minimax-gif-sticker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [GIF files delivered in a deliver_assets XML block with a brief status line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates four GIF stickers in fixed order: hi, laugh, cry, love; requires MiniMax API access and ffmpeg.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata says 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
