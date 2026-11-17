## Description:

Assist with HarmonyOS and OpenHarmony application development in ArkTS and ArkUI. Use when Codex needs to inspect, build, debug, refactor, review, or generate HarmonyOS projects, especially DevEco Studio or Stage model apps that use UIAbility, app.json5, module.json5, oh-package.json5, ohpm, hvigorw, hdc, permissions, routing, state management, HAP or HAR packaging, and signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louiseleven](https://clawhub.ai/user/louiseleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, build, debug, refactor, review, and generate HarmonyOS or OpenHarmony ArkTS projects. It is especially oriented toward DevEco Studio, Stage model apps, ArkUI, project configuration, permissions, routing, state management, packaging, and signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HarmonyOS code or configuration may request app permissions, use real network endpoints, or affect device deployment behavior.

Mitigation: Review generated code, permission declarations, endpoint usage, and build or install commands before granting permissions or deploying to devices.

Risk: Build and signing guidance may involve certificate material such as .p12 and .cer files.

Mitigation: Use project-approved signing configuration and avoid exposing or copying signing material into generated code, logs, or shared output.

Risk: The skill can suggest shell commands for ohpm, hvigorw, or hdc that modify dependencies, build outputs, or connected devices.

Mitigation: Prefer repository-provided scripts, inspect commands before execution, and report the exact verification boundary after running them.

## Reference(s):

- [HarmonyOS Developer](https://developer.harmonyos.com/)
- [OpenHarmony API Docs](https://docs.openharmony.cn/)
- [OpenHarmony App Samples](https://gitee.com/openharmony/app_samples)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with ArkTS, TypeScript, JSON5, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository inspection notes, module/page/config references, build commands, verification boundaries, and unverified device or signing steps.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-06-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
