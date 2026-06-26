## Description: <br>
Generate images and videos via Neodomain AI API, including text-to-image, image-to-video, text-to-video, universal multi-modal video, motion control video, and batch storyboard video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bandwhite](https://clawhub.ai/user/bandwhite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to choose Neodomain image or video generation workflows, format prompts and parameters, authenticate with an access token, and run the included Python helpers for media generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Neodomain access tokens and login contact details. <br>
Mitigation: Do not paste access tokens, login codes, personal contact details, or terminal output into shared chats or logs; store tokens only in appropriate local environment configuration. <br>
Risk: Prompts, source media, generated media, audio, and storyboard files may be sent to Neodomain and OSS-backed storage. <br>
Mitigation: Only upload content that is appropriate to share with the Neodomain service and related storage providers. <br>
Risk: Cloud generation output can be unexpected or unsuitable for a specific publication context. <br>
Mitigation: Review generated images, videos, thumbnails, and metadata before publishing, sharing, or using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/bandwhite/neo-ai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bandwhite) <br>
- [Skill source documentation](artifact/SKILL.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Neodomain image model endpoint](https://story.neodomain.cn/agent/ai-image-generation/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs may include image files, video files, thumbnails, and metadata JSON in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
