## Description: <br>
Interactive guide for integrating MobTech MobPush into HarmonyOS NEXT projects through a 6-step workflow with user confirmation before project changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add MobTech MobPush push notifications to HarmonyOS NEXT Stage-model ArkTS projects. It guides dependency installation, project configuration, Huawei push channel setup, privacy consent handling, message handling, and follow-up documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes edits to project configuration and source files that could be incorrect for a specific HarmonyOS project. <br>
Mitigation: Review every proposed command and file change before approval, and confirm the project path and Stage-model structure first. <br>
Risk: MobPush appKey and appSecret values may be stored in project configuration or source files. <br>
Mitigation: Avoid using production app secrets unless the project team accepts that storage pattern and has reviewed its source-control and release practices. <br>
Risk: Initializing MobPush before user privacy consent can create compliance issues. <br>
Mitigation: Follow the skill's consent-gated initialization flow and call the privacy authorization API only after the user agrees to the app privacy policy. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/mobsupport/harmonyos-mobpush-integration) <br>
- [Mob documentation center](https://www.mob.com/wiki/list) <br>
- [MobPush HarmonyOS integration guide](https://www.mob.com/wiki/detailed?wiki=697&id=136) <br>
- [MobPush SDK API reference](https://www.mob.com/wiki/detailed?wiki=698&id=136) <br>
- [MobPush backend configuration guide](https://www.mob.com/wiki/detailed?wiki=560&id=136) <br>
- [MobPush HarmonyOS compliance guide](https://www.mob.com/wiki/detailed?wiki=745&id=136) <br>
- [AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html) <br>
- [MobPush SDK privacy policy](https://policy.zztfly.com/sdk/mobpush/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, ArkTS snippets, JSON5 configuration examples, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before each project change and may generate a MobPush Excel configuration template plus project README.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
