## Description: <br>
A manga-animation workflow that guides an agent through script writing, storyboard design, character and style setup, storyboard image generation, and image-to-video generation with confirmation checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a574824551](https://clawhub.ai/user/a574824551) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and agent users can use this skill to turn a story idea or script into a staged manga-animation production plan, then generate character references, storyboard frames, and short video clips through Volcengine Ark APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends prompts, storyboard content, and image references to Volcengine Ark for media generation. <br>
Mitigation: Avoid submitting private scripts, proprietary images, or sensitive character references unless third-party processing is acceptable. <br>
Risk: ARK_API_KEY can be configured in source files, which may expose credentials if files are shared. <br>
Mitigation: Use an environment variable or local secret handling instead of editing API keys into source code. <br>
Risk: Generated images or videos can be low quality, inconsistent, or more expensive to regenerate after later stages. <br>
Mitigation: Review each checkpoint, especially storyboard and character-reference outputs, before moving to media generation. <br>


## Reference(s): <br>
- [Script Template](references/script-template.md) <br>
- [Storyboard Guide](references/storyboard-guide.md) <br>
- [Character Guide](references/character-guide.md) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON storyboard data, Python configuration edits, shell commands, generated image files, generated MP4 files, and generation logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged user checkpoints before cost-incurring media generation; generated media depends on the configured Ark API key, selected model, prompts, and source images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
