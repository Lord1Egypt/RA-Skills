## Description: <br>
Harmonyos Skill helps developers build, debug, migrate, optimize, and prepare HarmonyOS, ArkTS, and ArkUI applications for AppGallery publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fff-119](https://clawhub.ai/user/fff-119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for HarmonyOS application work, including ArkTS syntax guidance, ArkUI component design, API migration, compile error diagnosis, code quality checks, multi-device adaptation, performance optimization, and AppGallery Connect publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install scripts may copy prompt and configuration files into project-level or AI-tool configuration directories. <br>
Mitigation: Review the scripts before running them, install only the target tool you use, and keep backups of existing AI-tool configuration files. <br>
Risk: The build script removes and recreates the generated dist directory. <br>
Mitigation: Run the build script from the skill artifact directory and avoid storing hand-edited files in the generated dist folder. <br>
Risk: HarmonyOS guidance and generated code may be incomplete for a local project, device, SDK, or third-party package version. <br>
Mitigation: Review proposed code, run project builds and device tests, and confirm third-party SDK behavior against authoritative documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fff-119/skills/harmonyos-skill) <br>
- [ArkTS core programming patterns](references/arkts-patterns.md) <br>
- [ArkUI component usage patterns](references/arkui-components.md) <br>
- [ArkUI state management patterns](references/state-management.md) <br>
- [Huawei AppGallery Connect](https://developer.huawei.com/consumer/cn/service/jsp/agc/index.html) <br>
- [OpenHarmony Codelabs](https://gitee.com/openharmony/codelabs) <br>
- [OpenHarmony smart home demo collection](https://gitee.com/openharmony-sig/knowledge_demo_smart_home) <br>
- [OpenHarmony fun demo vendor project](https://gitee.com/openharmony-sig/vendor_oh_fun) <br>
- [HarmonyOS AudioSuiteSample](https://gitcode.com/HarmonyOS_Samples/guide-snippets/tree/HarmonyOS-7.0-beta-20260514/Media/Audio/AudioSuiteSample) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline ArkTS, TypeScript, JSON5, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include version-tagged code snippets, migration checklists, build or install commands, and AppGallery publishing guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
