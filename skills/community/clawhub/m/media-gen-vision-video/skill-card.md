## Description: <br>
Media Gen Vision Video guides agents through Google-native workflows for image generation and editing, multimodal image understanding, screenshot analysis, and Veo 3.1 video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielwpp](https://clawhub.ai/user/danielwpp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route image creation, image editing, visual analysis, screenshot inspection, and video generation requests through preferred Google media workflows while preserving media constraints and reporting blockers clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private screenshots, sensitive photos, or confidential media may be processed by external Google media services when the skill is used for generation, editing, analysis, or video workflows. <br>
Mitigation: Avoid using the skill with sensitive media unless the user is comfortable with those materials being processed by the external services described in the release evidence. <br>
Risk: Media generation or video workflows can fail or be unavailable in the current environment, creating a risk of overstating the result. <br>
Mitigation: State blockers clearly and only claim success when an actual generated image or video asset is available to return. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/danielwpp/media-gen-vision-video) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, files] <br>
**Output Format:** [Short Markdown response with generated media files or concise visual analysis when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image or video assets; reports blockers when media output is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
