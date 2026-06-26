## Description: <br>
代码沙箱 - 原创技能。安全执行未验证的AI生成代码，防止恶意代码、系统破坏或意外损害。适用于代码审查、安全验证、AI编程辅助等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as static review guidance for evaluating untrusted AI-generated code and planning sandbox controls before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes sandbox controls but does not provide or require an actual isolated runtime that enforces them. <br>
Mitigation: Use it as static review guidance unless a separately verified sandbox runtime provides network blocking, filesystem limits, resource caps, and cleanup. <br>
Risk: Untrusted code can damage systems or expose data if executed outside a real sandbox. <br>
Mitigation: Run untrusted code only in an isolated environment with outbound and inbound network access disabled, sensitive paths blocked, and strict CPU, memory, process, and disk limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-code-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides sandbox review checklists, risk patterns, sample configuration values, and execution report examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
