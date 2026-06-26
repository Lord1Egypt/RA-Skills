## Description: <br>
Auto-detects PC hardware details, estimates runnable LLM model sizes, and recommends quantization, deployment tools, and bottleneck optimizations with a Chinese output interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect local CPU, RAM, GPU, and VRAM details and get Chinese-language guidance on runnable LLM model sizes, quantization levels, deployment tools, and bottleneck fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardware probing can expose local system details such as CPU, RAM, GPU, VRAM, driver, and OS or WSL information in the agent session. <br>
Mitigation: Confirm that local hardware probing is intended before running the detector, and avoid sharing the output in untrusted contexts. <br>
Risk: The skill outputs in Chinese, which may be unsuitable for some users or reviewers. <br>
Mitigation: Ask the agent to translate or summarize the recommendations in the preferred language before acting on them. <br>
Risk: Model and quantization recommendations are heuristic and may not match every model build, runtime, or workload. <br>
Mitigation: Validate recommendations against the target model and deployment runtime documentation, then test with representative prompts before relying on the setup. <br>


## Reference(s): <br>
- [Hardware Llm Optimizer ClawHub page](https://clawhub.ai/smseow001/hardware-llm-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text in Chinese, usually presented as terminal output with recommendation lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local hardware details such as CPU, RAM, GPU, VRAM, driver, and OS or WSL information when the detector is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
