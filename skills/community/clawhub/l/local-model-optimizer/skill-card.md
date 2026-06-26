## Description: <br>
Auto-detects local hardware, recommends Ollama-compatible models, configures Ollama parameters, and sets up hybrid cloud/local routing in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate local AI hardware, choose a suitable Ollama model, estimate cost tradeoffs, and configure OpenClaw for local or hybrid model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The full auto workflow can install Ollama locally. <br>
Mitigation: Run detect or recommend first for read-only guidance, and run auto only after approving local installation. <br>
Risk: Model setup can download large Ollama model files. <br>
Mitigation: Check available disk space and network constraints before running auto or pulling recommended models. <br>
Risk: The skill can change OpenClaw configuration under ~/.openclaw. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before using auto or routing configuration commands. <br>


## Reference(s): <br>
- [Model Matrix](references/model-matrix.md) <br>
- [Ollama Model Library](https://ollama.com/library) <br>
- [ClawHub Release Page](https://clawhub.ai/stevojarvisai-star/local-model-optimizer) <br>
- [Publisher Profile](https://clawhub.ai/user/stevojarvisai-star) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify files under ~/.openclaw and may download Ollama models when the auto workflow is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
