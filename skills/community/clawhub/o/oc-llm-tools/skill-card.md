## Description: <br>
OpenClaw LLM Tools helps define LLM-callable tools once, validate tool-call arguments, and convert tool schemas for providers such as OpenAI, Anthropic, Gemini, and Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to register, validate, list, and convert LLM tool definitions across provider-specific function-calling formats. It is most relevant when one tool definition needs to be reused across multiple LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Side-effectful handlers registered by a user could change files, call APIs, or perform other actions when exposed to an LLM. <br>
Mitigation: Expose only reviewed handlers, validate arguments before execution, and require explicit confirmation before file-changing, API-changing, or other side-effectful calls. <br>
Risk: The skill documentation includes an eval-based calculator example that is unsafe to copy into production code. <br>
Mitigation: Do not reuse the eval pattern for untrusted input; replace it with a constrained parser or a reviewed calculation routine. <br>
Risk: The dependency declaration uses a broad jsonschema version range, which can reduce reproducibility. <br>
Mitigation: Pin dependencies when reproducible installs or audited deployments matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/oc-llm-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; CLI conversions can emit JSON tool-schema data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled CLI choices support OpenAI, Anthropic, Gemini, and Ollama conversion targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
