## Description: <br>
Generate ecommerce product video scripts from one or more product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, titles, and price stickers by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npai10](https://clawhub.ai/user/npai10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, marketers, and content teams use this skill to turn product images and optional selling points into short-form product video scripts and handoff notes for AI video generation with a default no-subtitles and no-text-overlay constraint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images and handoff prompts may be sent to an external video generation service after the user asks to generate video. <br>
Mitigation: Review the final handoff prompt and confirm that product images can be shared with the selected external service before submission. <br>
Risk: Generated video tools may still add subtitles, captions, UI text, or promotional text despite the script policy. <br>
Mitigation: Keep the explicit no-on-screen-text constraint in every handoff prompt and inspect generated videos before publishing. <br>
Risk: Research-enhanced scripts can overstate rankings, engagement, creator names, or current platform trends if sources are unavailable or incomplete. <br>
Mitigation: Use only cited research when available, label fallback outputs as unconnected to live research, and avoid exact metrics that were not verified. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/npai10/product-video-script-skill) <br>
- [Direction Playbook](references/direction-playbook.md) <br>
- [Output Template](references/output-template.md) <br>
- [Research Guide](references/research-guide.md) <br>
- [Video Handoff](references/video-handoff.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown scripts, direction options, research summaries, next actions, and video handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs default to 15-second 9:16 product-video scripts and preserve a no-subtitles, no-captions, and no-text-overlay policy unless the user explicitly changes requirements.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
