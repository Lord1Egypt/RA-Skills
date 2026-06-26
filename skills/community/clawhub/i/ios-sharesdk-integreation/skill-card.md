## Description: <br>
面向 iOS 工程的 MobTech ShareSDK 集成 skill。默认优先使用 CocoaPods，先扫描工程，再串行确认阻塞项，最后以最小改动完成接入、隐私合规与项目内说明文档落地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
iOS developers use this skill to integrate MobTech ShareSDK into existing iOS projects with CocoaPods, platform credential configuration, privacy-gated initialization, and minimal project changes. It supports scanning the project first, generating a ShareSDK_Config.xlsx template, validating credentials, and preparing configuration or code changes for enabled platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles MobTech and social-platform app credentials while preparing ShareSDK configuration. <br>
Mitigation: Install it only for the intended iOS project, keep credentials scoped to that project, and review generated configuration before applying it. <br>
Risk: The skill can modify project configuration files and propose CocoaPods dependency installation or updates. <br>
Mitigation: Review the proposed file changes first, and only allow pod install or pod update after confirming the plan. <br>


## Reference(s): <br>
- [MobTech ShareSDK iOS documentation](https://www.mob.com/wiki/detailed?wiki=4&id=14) <br>
- [MobTech ShareSDK iOS integration documentation](https://www.mob.com/wiki/detailed?wiki=500&id=14) <br>
- [MobTech ShareSDK related documentation](https://www.mob.com/wiki/detailed?wiki=499&id=14) <br>
- [MobTech ShareSDK platform documentation](https://www.mob.com/wiki/detailed?wiki=747&id=14) <br>
- [ShareSDK privacy policy](https://policy.zztfly.com/sdk/share/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a ShareSDK_Config.xlsx workbook and project integration notes; requires user confirmation before dependency installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
