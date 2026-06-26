## Description: <br>
Generates short first-person product promotion videos from product images and scripts using Volcengine Ark/Seedance, optional TTS, background music mixing, and burned-in subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agent operators use this skill to turn a product image and short script into a vertical product promotion video with voiceover, background music, subtitles, and a selected presenter persona. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use billable Ark/Seedance and optional Volcengine TTS credentials. <br>
Mitigation: Run dry-run first, review the estimated cost, and obtain user confirmation before full rendering. <br>
Risk: Product images and scripts may be sent to external AI or TTS services. <br>
Mitigation: Use only content approved for those services and avoid confidential or sensitive product material unless the user has authorized it. <br>
Risk: Generated videos may use local background music assets with separate rights requirements. <br>
Mitigation: Use properly licensed or royalty-free music and keep attribution where the music source requires it. <br>
Risk: Local output paths could overwrite important files. <br>
Mitigation: Choose explicit output paths in a working directory and review paths before running render commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-influencer-video-skill) <br>
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3) <br>
- [ByteDance OpenSpeech TTS](https://openspeech.bytedance.com) <br>
- [Pixabay Music](https://pixabay.com/music/) <br>
- [Freesound](https://freesound.org/) <br>
- [Incompetech royalty-free music](https://incompetech.com/music/royalty-free/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MP4 video files, JSON script files, Markdown guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated video files, voice audio, subtitles, cost estimates, token estimates, template selections, and local file paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
