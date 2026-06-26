## Description: <br>
Implements a JavaScript literal syntax-based protocol for LLM tool calls. Invoke when needing to enable LLM to call local JS functions using template literal syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roryyu](https://clawhub.ai/user/roryyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define a JavaScript template-literal protocol that lets an LLM call local JavaScript tag functions with interpolated arguments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model-generated template-literal calls could invoke local functions with side effects if executed without validation. <br>
Mitigation: Treat model output as data until validated, expose only a small allowlist of safe tag functions, sandbox execution, validate arguments, and require user approval for functions that read files, use secrets, access the network, mutate data, or run commands. <br>
Risk: The skill describes a protocol pattern but does not provide runtime enforcement. <br>
Mitigation: Implementers should add their own parser, executor controls, argument validation, and permission checks before using the pattern with local functions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roryyu/js-literals-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for JavaScript tag-function tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
