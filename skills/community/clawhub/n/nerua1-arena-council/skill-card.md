## Description: <br>
Multi-Model Council - parallel execution of multiple LLMs with voting/consensus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to query multiple local LM Studio language models in parallel and combine their answers with weighted or majority voting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may integrate with refusal-bypass prompt rewriting when sibling God Mode files are present. <br>
Mitigation: Install only when that behavior is intended; remove or disable the God Mode integration for ordinary consensus use. <br>
Risk: Prompts and model outputs are sent to every selected local model and may be exposed through trusted or untrusted local model runtimes and logs. <br>
Mitigation: Avoid sensitive prompts unless every configured local model, runtime, and log path is trusted. <br>
Risk: Automatic model probing can execute behavior from sibling God Mode files if they exist in the workspace. <br>
Mitigation: Review any sibling God Mode files before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/nerua1-arena-council) <br>
- [LM Studio local OpenAI-compatible API endpoint](http://127.0.0.1:1234/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a consensus response from local model outputs; raw per-model responses are available through the implementation API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
