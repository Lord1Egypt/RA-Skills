## Description: <br>
Generate ecommerce product video scripts from one or more product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, titles, and price stickers by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npai10](https://clawhub.ai/user/npai10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, ecommerce operators, and agent users use this skill to turn product images and optional selling points into concise short-video scripts, direction choices, voiceover copy, and video handoff notes. It is designed for commerce video workflows that need scripts without generated subtitles or on-screen text overlays by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoff prompts may still need review before product images are sent to an external video generation tool, especially when strict no on-screen text is required. <br>
Mitigation: Review the generated handoff notes and preserve the no-subtitles and no-text-overlay constraints before submitting any video task. <br>
Risk: Research-enhanced scripts can be incomplete when live browsing is unavailable or exact platform metrics cannot be verified. <br>
Mitigation: Use the skill's fallback labeling and avoid unverified rankings, likes, creator names, or video URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npai10/product-video-script-skill-no-subtitles) <br>
- [Direction Playbook](references/direction-playbook.md) <br>
- [Output Template](references/output-template.md) <br>
- [Research Guide](references/research-guide.md) <br>
- [Video Handoff](references/video-handoff.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown script drafts with voiceover, visual-flow notes, direction options, next actions, and video handoff constraints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 15-second 9:16 product-video scripts and no subtitles, captions, title cards, price stickers, floating labels, or generated text overlays unless the user changes constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
