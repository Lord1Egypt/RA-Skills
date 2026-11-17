## Description:

Generates ecommerce product video scripts from product images and optional selling points, with handoff guidance that forbids subtitles, captions, text overlays, titles, and price stickers by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npai10](https://clawhub.ai/user/npai10)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and marketing teams use this skill to turn product images and selling points into short-form product video scripts and video handoff notes for platforms such as TikTok, Douyin, Xiaohongshu, and livestream commerce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images or product details may be sent to an external video generation tool during handoff.

Mitigation: Review the user's consent and the generated handoff prompt before submitting assets; video generation should start only after an explicit request.

Risk: Generated videos may accidentally include subtitles, overlays, price stickers, or new text.

Mitigation: Check the handoff prompt and final output against the no-subtitle and no-text-overlay policy before use.

Risk: Research-based scripts may overstate trends or platform performance when sources are incomplete.

Mitigation: Use cited sources, avoid unverifiable likes or rankings, and label fallback scripts when live research was not performed.

## Reference(s):

- [Direction Playbook](references/direction-playbook.md)
- [Output Template](references/output-template.md)
- [Research Guide](references/research-guide.md)
- [Video Handoff](references/video-handoff.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown scripts, voiceover text, direction options, and video handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default script target is a 15-second 9:16 video; video generation handoff is gated on explicit user request; no subtitles or generated on-screen text by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
