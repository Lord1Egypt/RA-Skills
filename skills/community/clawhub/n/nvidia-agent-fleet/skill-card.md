## Description: <br>
Routes prompts to a fleet of NVIDIA API-backed model agents, with automatic task classification, single-agent dispatch, and optional parallel multi-agent execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to choose among specialized NVIDIA-hosted model agents for coding, reasoning, writing, Chinese-language, research, finance, vision, embedding, and quick-response tasks. It supports CLI and Python workflows for automatic routing, explicit agent selection, task analysis, and multi-agent comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic credential discovery may execute a local shell startup file while looking for NVIDIA_API_KEY. <br>
Mitigation: Set NVIDIA_API_KEY explicitly in the environment and avoid relying on shell startup file discovery. <br>
Risk: The skill may read local OpenClaw configuration files while searching for NVIDIA credentials. <br>
Mitigation: Review local configuration files before use and run the skill only in an environment where that credential lookup is acceptable. <br>
Risk: Prompts are sent to NVIDIA API endpoints during dispatch. <br>
Mitigation: Use the skill only with prompts and data that may be sent to NVIDIA APIs under your applicable policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/nvidia-agent-fleet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Python return objects containing model content, usage metadata, selected agent details, and errors when calls fail.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call NVIDIA API endpoints using NVIDIA_API_KEY; multi-agent mode can run selected agents in parallel with per-model timeouts.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
