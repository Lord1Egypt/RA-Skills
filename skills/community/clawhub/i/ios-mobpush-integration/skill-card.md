## Description: <br>
面向 iOS 工程的 MobTech MobPush 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成推送依赖接入、APNs 配置、隐私合规、回调接线和项目内说明文档落地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and iOS engineers use this skill to integrate or troubleshoot MobTech MobPush in existing iOS apps with minimal project changes. It guides project scanning, CocoaPods setup, APNs configuration, privacy consent wiring, notification callbacks, and project documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read iOS project files and propose or apply changes to build settings, dependencies, source code, and plist configuration. <br>
Mitigation: Review the proposed change plan before approval, keep the work in version control, and inspect generated diffs before relying on the integration. <br>
Risk: MobPush appKey and appSecret are project secrets that may be written into configuration files during integration. <br>
Mitigation: Treat these values as secrets, avoid sharing them in prompts or logs, and confirm the target plist and repository policy before approving changes. <br>
Risk: Dependency installation through CocoaPods can modify dependency state and project workspace files. <br>
Mitigation: Approve CocoaPods installation only when ready for dependency changes, then review Podfile and Podfile.lock updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobsupport/ios-mobpush-integration) <br>
- [MobTech documentation center](https://www.mob.com/wiki/list) <br>
- [MobPush product page](https://www.mob.com/mobService/mobpush) <br>
- [MobTech SDK download center](https://www.mob.com/download) <br>
- [MobPush app creation guide](https://www.mob.com/wiki/detailed?wiki=494&id=136) <br>
- [MobPush compliance guide](https://www.mob.com/wiki/detailed?wiki=501&id=136) <br>
- [MobPush integration guide](https://www.mob.com/wiki/detailed?wiki=502&id=136) <br>
- [MobPush SDK API documentation](https://www.mob.com/wiki/detailed?wiki=503&id=136) <br>
- [MobPush certificate configuration](https://www.mob.com/wiki/detailed?wiki=504&id=136) <br>
- [MobPush extension feature setup](https://www.mob.com/wiki/detailed?wiki=665&id=136) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and generated project documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate an Excel configuration template and a project-level MobPush_README.md when used in an iOS project.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
