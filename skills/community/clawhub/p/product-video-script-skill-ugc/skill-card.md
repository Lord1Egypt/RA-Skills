## Description: <br>
Generate ecommerce product video scripts from one or more product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, titles, and price stickers by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npai10](https://clawhub.ai/user/npai10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and ecommerce teams use this skill to turn product images and selling points into short-form product video scripts and video handoff notes. It is designed for platform-ready commerce concepts, including TikTok-style UGC, livestream selling, comparison, promotion, and TVC-style directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images and generated scripts may be shared with a downstream video generation tool if the user later asks to generate video. <br>
Mitigation: Use only video tools and projects approved for the product material, and confirm that sharing product images and scripts is acceptable before generation. <br>
Risk: A downstream video model may not fully honor the strict no-subtitles or no-text-overlay requirement. <br>
Mitigation: Review generated videos before use and reject or regenerate outputs that add subtitles, captions, text overlays, title cards, price stickers, floating labels, or generated UI text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npai10/product-video-script-skill-ugc) <br>
- [Direction Playbook](references/direction-playbook.md) <br>
- [Output Template](references/output-template.md) <br>
- [Research Guide](references/research-guide.md) <br>
- [Video Handoff](references/video-handoff.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown scripts with voiceover, visual flow, next actions, and video handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 15-second 9:16 short-video scripts and forbids added subtitles, captions, text overlays, title cards, price stickers, floating labels, and generated UI text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
