## Description: <br>
Hardware LLM Optimizer v2 uses llmfit to inspect CPU, GPU, RAM, and VRAM, then recommend suitable local LLMs, quantization plans, and speed estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose local LLMs and quantization settings for available or simulated hardware before installing or running models with tools such as Ollama or llama.cpp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an unverified remote installer that can execute code on the user's machine. <br>
Mitigation: Review the installer path before use and prefer Homebrew, uv/pip, Docker, or a manually downloaded release with checksum or signature verification instead of running the curl-piped shell command. <br>
Risk: The tool may inspect and display hardware details such as CPU, RAM, GPU, VRAM, and driver information. <br>
Mitigation: Run it only in environments where exposing local hardware details is acceptable, and avoid sharing generated reports when they contain sensitive system information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/hardware-llm-optimizer-v2) <br>
- [llmfit installer script](https://llmfit.axjns.dev/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with command snippets and optional JSON output from llmfit] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model names, quantization choices, estimated tokens per second, memory requirements, fit scores, and hardware details.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
