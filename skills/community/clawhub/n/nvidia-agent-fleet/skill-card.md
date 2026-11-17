## Description:

Routes user tasks to a registry of NVIDIA API-backed model agents, with automatic task classification, selected-agent execution, and optional multi-agent parallel responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route prompts to task-specific NVIDIA API model agents for coding, reasoning, Chinese-language tasks, writing, research, quick summaries, and multi-agent comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic credential discovery can read local credential files and run shell configuration while looking for NVIDIA_API_KEY.

Mitigation: Set NVIDIA_API_KEY explicitly and avoid installing or running the skill in environments where shell startup files have side effects.

Risk: Prompt content is transmitted to NVIDIA's API during model calls.

Mitigation: Do not submit secrets, regulated data, or private business data unless the deployment has approved handling for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/nvidia-agent-fleet)
- [Publisher profile](https://clawhub.ai/user/clementgu)
- [NVIDIA API endpoint](https://integrate.api.nvidia.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Python dictionaries containing model responses, usage data, selected agents, and timing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on selected model agents, NVIDIA_API_KEY availability, configured max token limits, and per-model request timeouts.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
