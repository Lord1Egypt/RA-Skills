## Description: <br>
Helps agents recommend local LLM models, quantization options, and runtime choices based on hardware and use case using llmfit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bshaot](https://clawhub.ai/user/bshaot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local LLM users use this skill to ask an agent for hardware-aware model recommendations for coding, chat, reasoning, general, multimodal, or embedding workflows, including suggested quantization and runtime options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to run llmfit commands that inspect local hardware for recommendations. <br>
Mitigation: Review the suggested command and its output before execution, and avoid sharing hardware details outside trusted local workflows. <br>
Risk: The skill may suggest update scripts or Docker commands that rely on external tools not bundled with the skill package. <br>
Mitigation: Inspect scripts, Docker images, source locations, and command arguments before running them; use trusted llmfit releases and container images. <br>


## Reference(s): <br>
- [llmfit documentation](https://github.com/AlexsJones/llmfit) <br>
- [Hugging Face model library](https://huggingface.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest llmfit commands that inspect local hardware or use external llmfit and Docker tooling; no executable code is bundled in the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
