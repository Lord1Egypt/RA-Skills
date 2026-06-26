## Description: <br>
OpenHarmony React Native performance static checks and optimization guidance for reviewing RNOH code, bundle-harmony configuration, lifecycle wiring, TurboModule placement, and React rendering patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[code-sunbo](https://clawhub.ai/user/code-sunbo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to review React Native for OpenHarmony applications for performance-sensitive render, lifecycle, bundle, list, and TurboModule patterns. It supports static analysis and code review by pointing agents to focused rule files and concrete examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied production bundle or Hermes bytecode commands may be inappropriate for a specific build pipeline. <br>
Mitigation: Review command flags and output paths before applying them to production or CI projects. <br>
Risk: TurboModule worker guidance can hurt performance if UI-bound modules are moved off the main thread. <br>
Mitigation: Apply worker-thread configuration only to heavy or I/O-bound modules and keep UI-bound modules on the appropriate thread. <br>


## Reference(s): <br>
- [OpenHarmony-SIG homecheck repository](https://gitcode.com/openharmony-sig/homecheck) <br>
- [OpenHarmony React Native performance optimization documentation (English)](https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/en/performance-optimization.md) <br>
- [OpenHarmony React Native performance optimization documentation (Chinese)](https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/zh-cn/%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98.md) <br>
- [ClawHub skill page](https://clawhub.ai/code-sunbo/ohos-react-native-performance) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/code-sunbo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no hidden execution or data access was reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
