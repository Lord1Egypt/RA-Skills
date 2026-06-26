## Description: <br>
Generate music and audio via Kie.ai's Suno gateway for background tracks, instrumental beds, full songs with vocals, or extending existing audio clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benhuebner01](https://clawhub.ai/user/benhuebner01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or extend music and audio assets through Kie.ai/Suno from prompts or source audio URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw global environment secrets instead of only the Kie credentials it needs. <br>
Mitigation: Run it in an isolated OpenClaw profile containing only KIE_API_KEY and, when webhook verification is needed, KIE_WEBHOOK_HMAC_KEY. <br>
Risk: Prompts, lyrics, and extension audio URLs are sent to Kie.ai/Suno. <br>
Mitigation: Confirm the content is appropriate to share with that service before running generation or extension requests. <br>
Risk: Generation requests may spend API credits and write media files locally. <br>
Mitigation: Confirm the request before execution and use an explicit output directory for generated files. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/benhuebner01/kie-audio) <br>
- [Kie.ai API key setup](https://kie.ai/api-key) <br>
- [Kie.ai API endpoint](https://api.kie.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files] <br>
**Output Format:** [JSON status containing the task ID and downloaded audio and cover-image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads one or more audio tracks and optional cover images to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
