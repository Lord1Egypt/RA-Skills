## Description: <br>
Adds voice-over and styled subtitles to videos by collecting video, transcript, voice, speed, and subtitle style inputs and calling a Coze workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to add dubbing and readable subtitles to videos, choose preset or custom subtitle styling, adjust speech speed, and receive a processed video URL. It is suited to public or non-sensitive video workflows where sending a video URL and transcript to Coze is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user video URLs and subtitle text to a third-party Coze workflow. <br>
Mitigation: Use only public or non-sensitive videos and provide a clear privacy notice before processing. <br>
Risk: The evidence security summary reports an embedded Coze bearer token. <br>
Mitigation: Remove and rotate the embedded token, then require credentials from secure configuration before deployment. <br>


## Reference(s): <br>
- [Subtitle style configuration](references/subtitle-styles.md) <br>
- [ClawHub release page](https://clawhub.ai/golngod/opc-video-subtitle-tool) <br>
- [Coze platform](https://coze.cn) <br>
- [Voice ID reference](https://x2hx0ilo74.feishu.cn/wiki/QJCVwnbr1iBOkzkllk6cS6tCnZe) <br>
- [Custom subtitle parameter reference](https://my.feishu.cn/wiki/TumOwWKFNiTr19ky36Vc7bXZnLc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a processed video URL from the Coze workflow when execution succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
