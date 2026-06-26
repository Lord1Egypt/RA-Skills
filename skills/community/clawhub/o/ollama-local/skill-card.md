## Description: <br>
Manage and use local Ollama models. Use for model management (list/pull/remove), chat/completions, embeddings, and tool-use with local LLMs. Covers OpenClaw sub-agent integration and model selection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Timverhoogt](https://clawhub.ai/user/Timverhoogt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Ollama models, run local chat or completion requests, create embeddings, and test tool-use workflows through OpenClaw sub-agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, completions, embeddings, and tool-use requests may be sent to a configured remote Ollama server. <br>
Mitigation: Keep OLLAMA_HOST on localhost for sensitive prompts, use only trusted remote Ollama servers, and confirm the target host before sending requests. <br>
Risk: Model pull, removal, and sub-agent workflows can consume disk or network resources, or remove local model files. <br>
Mitigation: Double-check the target host and model name before running pull, rm, or sub-agent workflows. <br>


## Reference(s): <br>
- [Model Guide](references/models.md) <br>
- [Ollama Local on ClawHub](https://clawhub.ai/Timverhoogt/ollama-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and command output from Ollama helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream model responses and print model metadata, embeddings summaries, or tool-call traces depending on the selected command.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
