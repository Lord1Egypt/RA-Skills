## Description: <br>
Detect local hardware (RAM, CPU, GPU/VRAM) and recommend the best-fit local LLM models with optimal quantization, speed estimates, and fit scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexsJones](https://clawhub.ai/user/AlexsJones) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local hardware capacity, choose local LLMs that fit available RAM or VRAM, and configure OpenClaw providers such as Ollama, vLLM, or LM Studio with an appropriate model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external llmfit CLI to inspect local hardware details. <br>
Mitigation: Install and run the CLI only when the user is comfortable trusting that local hardware inspection. <br>
Risk: Model provider recommendations may change OpenClaw configuration, including the default local model. <br>
Mitigation: Review proposed openclaw.json changes and require explicit approval before applying model or provider settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlexsJones/llmfit) <br>
- [Publisher profile](https://clawhub.ai/user/AlexsJones) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hardware summaries, ranked model recommendations, quantization guidance, speed estimates, and OpenClaw provider configuration suggestions.] <br>

## Skill Version(s): <br>
0.2.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
