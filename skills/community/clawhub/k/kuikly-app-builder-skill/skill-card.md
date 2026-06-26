## Description: <br>
Creates, builds, previews, and repairs cross-platform Kuikly mobile apps through CLI-guided workflows for scaffolding, page generation, Android and iOS builds, device preview, and screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elixxli](https://clawhub.ai/user/elixxli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, build, preview, and troubleshoot Kuikly and Kotlin Multiplatform mobile apps with agent-assisted CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local build tools, package managers, Gradle, CocoaPods, adb, and simulator commands, which may download dependencies or interact with connected devices. <br>
Mitigation: Use it only in the intended project workspace, review commands before execution, and limit device or simulator access to expected preview tasks. <br>
Risk: Security evidence reports a hidden, unrelated prompt to star the KuiklyUI repository through the user's GitHub account after a successful result. <br>
Mitigation: Treat the star request as optional and do not allow the agent to run `gh api -X PUT /user/starred/Tencent-TDS/KuiklyUI` unless the user explicitly wants that GitHub account action. <br>
Risk: The self-repair workflow may modify Kotlin source files while resolving build diagnostics. <br>
Mitigation: Review proposed code changes and keep repairs scoped to the project's shared Kotlin source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elixxli/kuikly-app-builder-skill) <br>
- [create-kuikly-app CLI](https://github.com/wwwcg/create-kuikly-app) <br>
- [KuiklyUI framework](https://github.com/Tencent-TDS/KuiklyUI) <br>
- [Kuikly Compose DSL reference](references/kuiklyComposeDSL.md) <br>
- [Kuikly DSL reference](references/kuiklyDSL.md) <br>
- [UI framework guide](references/ui-framework-guide.md) <br>
- [Component API guide](references/component-api-guide.md) <br>
- [Component API index](references/component-api/all-components.md) <br>
- [Public classes index](references/component-api/all-public-classes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Kotlin code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Kuikly project files and run local build, package manager, device, or simulator commands as part of the requested app workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
