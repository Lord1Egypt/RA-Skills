## Description: <br>
Runs local Ollama prompt tests against dataset samples so developers can compare model and prompt behavior without using cloud services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBlockChainNetwork](https://clawhub.ai/user/GBlockChainNetwork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to run local Ollama prompt or model checks on dataset samples, inspect short responses, and iterate on prompts or Modelfiles before adopting broader tuning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes model and LoRA tuning, while the artifact behavior is a lightweight local prompt-evaluation helper. <br>
Mitigation: Treat it as prompt-testing guidance unless a separate, reviewed fine-tuning workflow is provided. <br>
Risk: Dataset prompts are sent to the configured Ollama service during local evaluation. <br>
Mitigation: Use only datasets approved for that Ollama environment and avoid sensitive data unless local service controls are acceptable. <br>
Risk: Execution depends on the local runnable command and the Python ollama package. <br>
Mitigation: Review dependencies and run the helper in a controlled local environment before using it with important datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBlockChainNetwork/ollama-model-tuner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Ollama command suggestions and short prompt-evaluation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
