## Description: <br>
NVIDIA Agent Fleet routes prompts to a registry of NVIDIA-hosted model agents, including task analysis, single-agent dispatch, and optional multi-agent parallel execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to route coding, reasoning, writing, research, Chinese-language, and other prompt tasks to selected NVIDIA API models. It supports CLI and Python SDK workflows for listing agents, analyzing task fit, dispatching to a specified or recommended agent, and running multiple agents serially or in parallel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically searches local credential stores and executes the user's shell startup file while looking for NVIDIA_API_KEY. <br>
Mitigation: Set NVIDIA_API_KEY explicitly in the current environment and review or disable automatic credential discovery before installing in managed environments. <br>
Risk: Normal use sends task content to NVIDIA's API. <br>
Mitigation: Do not include secrets, private code, or regulated data in prompts unless the target environment and API terms permit that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/nvidia-agent-fleet) <br>
- [NVIDIA API endpoint used by the dispatcher](https://integrate.api.nvidia.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text from CLI runs and JSON-like Python dictionaries from SDK calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected model and configured token limits; multi-agent mode returns one response per successful agent.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
