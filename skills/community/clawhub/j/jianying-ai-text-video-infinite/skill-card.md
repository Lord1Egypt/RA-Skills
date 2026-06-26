## Description: <br>
自动化操作剪映桌面客户端，将用户提供的分镜脚本通过 AI 文字成片功能生成 9:16 比例未来科幻风格视频，并配置真人播客女配音。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to drive the Jianying desktop client and turn a user-provided storyboard script into a configured AI text-to-video project. It is intended for Windows desktop sessions where Jianying is installed, focused, and ready for coordinate-based automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the Windows desktop and may click the wrong target if Jianying is not focused or the user interacts with the computer during automation. <br>
Mitigation: Keep Jianying open and focused, avoid using the computer during automation, and require user confirmation before starting video generation. <br>
Risk: The skill overwrites clipboard contents and text fields while inserting the storyboard script. <br>
Mitigation: Treat clipboard contents as temporary during execution and review the target text field before approving generation. <br>
Risk: The skill can save screenshots and temporary files during verification. <br>
Mitigation: Review and delete generated screenshots or temporary files after the run if they contain sensitive project content. <br>
Risk: The skill may install dependencies or modify skill files as part of its workflow. <br>
Mitigation: Require explicit approval before dependency installation or skill-file self-modification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/jianying-ai-text-video-infinite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates a Windows desktop client through fixed screen coordinates, clipboard input, and confirmation-gated video generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
