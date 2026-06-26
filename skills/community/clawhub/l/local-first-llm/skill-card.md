## Description: <br>
Routes LLM requests to a local model (Ollama, LM Studio, llamafile) before falling back to cloud APIs and tracks token savings and cost avoidance in a persistent dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelnishanth](https://clawhub.ai/user/joelnishanth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to decide whether an LLM request should run on a local provider or fall back to cloud APIs, then record routing outcomes and token-cost savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud fallback may send prompts to external APIs when no local provider is available or when the request is classified as high complexity. <br>
Mitigation: Confirm whether cloud fallback is acceptable before use, and choose a local-only operating mode for sensitive prompts where available. <br>
Risk: The provider setup reference includes a curl-to-shell installer pattern for Ollama. <br>
Mitigation: Prefer package managers, signed releases, or review and verify installer contents before running remote installation commands. <br>
Risk: Savings history is written to a local user file under the home directory. <br>
Mitigation: Review local retention expectations and reset the savings log when persistent request metadata should not be kept. <br>


## Reference(s): <br>
- [Routing Decision Logic](references/routing-logic.md) <br>
- [Local LLM Provider Setup](references/local-providers.md) <br>
- [Token Estimation & Cloud Cost Reference](references/token-estimation.md) <br>
- [LM Studio](https://lmstudio.ai) <br>
- [llamafile Releases](https://github.com/Mozilla-Ocho/llamafile/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts to check provider availability, route requests, log outcomes, and display cumulative savings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
