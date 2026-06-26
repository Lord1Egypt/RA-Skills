## Description: <br>
Find the best local LLM for your machine. Tests speed, quality and RAM fit, then tells you if a model is worth running on your hardware. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheBlueHouse75](https://clawhub.ai/user/TheBlueHouse75) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and local LLM users use this skill to benchmark a named Ollama or LM Studio model on their own hardware and decide whether it is worth running. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmarks can consume local CPU, GPU, RAM, and time. <br>
Mitigation: Run benchmarks when the machine has enough available resources and close GPU-intensive applications first. <br>
Risk: Shared leaderboard results can disclose model, score, CPU, RAM, and GPU details. <br>
Mitigation: Use --share only when publishing those hardware and benchmark details is acceptable. <br>
Risk: The workflow depends on the third-party MetriLLM npm package and local model servers. <br>
Mitigation: Install only if the package and source are trusted, and keep Ollama or LM Studio under local user control. <br>


## Reference(s): <br>
- [MetriLLM ClawHub page](https://clawhub.ai/TheBlueHouse75/metrillm) <br>
- [MetriLLM community leaderboard](https://metrillm.dev) <br>
- [Ollama](https://ollama.com) <br>
- [LM Studio](https://lmstudio.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON benchmark output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save benchmark results locally; optional sharing can publish model, score, CPU, RAM, and GPU details.] <br>

## Skill Version(s): <br>
0.2.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
