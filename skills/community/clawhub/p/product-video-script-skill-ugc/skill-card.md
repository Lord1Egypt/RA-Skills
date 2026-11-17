## Description:

Generate ecommerce product video scripts from one or more product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, titles, and price stickers by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npai10](https://clawhub.ai/user/npai10)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and marketing teams use this skill to turn product images and optional selling points into short-form product video scripts, direction options, voiceover copy, and video handoff notes. It is especially oriented toward TikTok-style UGC ads and Chinese ecommerce script directions while keeping generated video text overlays disabled by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route product images and scripts into an external LibTV video-generation workflow.

Mitigation: Confirm the intended provider, uploaded assets, and generated-script content before selecting any video-generation action.

Risk: Users may not intend to transfer product images or scripts outside the scripting workflow.

Mitigation: Use the skill for script drafting only unless the user explicitly asks to generate video and accepts the external handoff.

Risk: Research-based scripts can overstate platform trends or performance when current sources are unavailable.

Mitigation: Use cited research when browsing is available; otherwise label the result as an offline version and avoid invented rankings, likes, creator names, or video URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npai10/skills/product-video-script-skill-ugc)
- [Direction Playbook](artifact/references/direction-playbook.md)
- [Output Template](artifact/references/output-template.md)
- [Research Guide](artifact/references/research-guide.md)
- [Video Handoff](artifact/references/video-handoff.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured sections for product diagnosis, direction options, scripts, voiceover, video handoff notes, variants, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Chinese and English script content; default script targets are 15-second, 9:16 short-form videos unless the user requests otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
