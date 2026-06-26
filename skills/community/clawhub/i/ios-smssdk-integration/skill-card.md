## Description: <br>
面向 iOS 工程的 MobTech SMSSDK 短信验证集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成依赖接入、隐私合规、短信验证码发送/校验链路和项目内说明文档落地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
iOS developers use this skill to integrate or troubleshoot MobTech SMSSDK SMS verification in existing apps. It helps scan the project, plan minimal changes, configure dependencies and privacy settings, wire verification-code send and submit flows, and document the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose and apply edits to iOS project files such as Podfile, Info.plist, bridge or wrapper code, and project documentation. <br>
Mitigation: Review the proposed change plan and resulting diffs before accepting changes. <br>
Risk: Dependency installation and build commands such as pod install or xcodebuild can change local project state or require broader filesystem access. <br>
Mitigation: Run those commands only after confirming they are expected for the current project. <br>
Risk: MOBAppKey, MOBAppSecret, and privacy compliance settings are sensitive project configuration. <br>
Mitigation: Keep credentials out of source code where possible and verify privacy settings with the project owner before release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mobsupport/ios-smssdk-integration) <br>
- [MobTech 文档中心](https://www.mob.com/wiki/list) <br>
- [SDK 下载中心](https://www.mob.com/download) <br>
- [创建应用](https://www.mob.com/wiki/detailed?wiki=539&id=23) <br>
- [集成指南](https://www.mob.com/wiki/detailed?wiki=110&id=23) <br>
- [SDK API 文档](https://www.mob.com/wiki/detailed?wiki=467&id=23) <br>
- [合规指南](https://www.mob.com/wiki/detailed?wiki=211&id=23) <br>
- [SMSSDK 扩展业务功能设置](https://www.mob.com/wiki/detailed?wiki=671&id=23) <br>
- [错误码](https://www.mob.com/wiki/detailed?wiki=468&id=23) <br>
- [App Store Connect 后台隐私数据项配置](https://www.mob.com/wiki/detailed?wiki=573&id=23) <br>
- [其它 App 数据采集主动控制器配置](https://www.mob.com/wiki/detailed?wiki=675&id=714) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese user-facing responses and asks for confirmation before dependency installation or build commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
