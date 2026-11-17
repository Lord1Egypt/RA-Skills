## Description:

Generates ecommerce product video scripts from product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, title cards, and price stickers by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npai10](https://clawhub.ai/user/npai10)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketers, and content creators use this skill to turn product images and optional selling points into short-form product video scripts, direction options, research summaries when available, and approval-gated video handoff notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images and script details may be handed to a video-generation tool after the user approves generation.

Mitigation: Require explicit user approval before video handoff and include only the product references and confirmed script details needed for that task.

Risk: Research-based or competitor-based script requests can lead to unsupported claims about rankings, likes, creators, or performance.

Mitigation: Cite sources when research is used, avoid inventing exact metrics, and label fallback outputs when browsing is unavailable.

Risk: The skill includes Chinese ecommerce terminology and platform directions that may not fit every market.

Mitigation: Localize language, platform framing, campaign references, and calls to action before use outside the intended market.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npai10/skills/product-video-script-skill)
- [Direction Playbook](references/direction-playbook.md)
- [Output Template](references/output-template.md)
- [Research Guide](references/research-guide.md)
- [Video Handoff](references/video-handoff.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured product diagnosis, direction options, script sections, optional research summary, next actions, and video handoff notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default script target is a concise 15-second 9:16 product video unless the user specifies otherwise; video generation is gated on explicit user approval.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
