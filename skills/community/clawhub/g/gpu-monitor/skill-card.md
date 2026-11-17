## Description:

Provides real-time NVIDIA GPU usage and memory stats, plus Ollama model layer GPU/CPU distribution via server.log parsing with live updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkerjueberg](https://clawhub.ai/user/tinkerjueberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor local NVIDIA GPU memory, utilization, and temperature while running workloads. Users running Ollama can also inspect model layer placement between GPU and CPU when a server.log path is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a long-running local GPU monitor and repeatedly call nvidia-smi.

Mitigation: Run it only in a trusted local environment and choose an update interval that is appropriate for the host.

Risk: When configured with an Ollama server.log path, the skill reads local log data.

Mitigation: Point it only at the intended local Ollama log and avoid using logs that contain sensitive prompts, paths, or operational details.

Risk: The artifact includes an entrypoint helper that can overwrite entry.py.

Mitigation: Review or remove the create_entry_script behavior before using the skill in a managed environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tinkerjueberg/skills/gpu-monitor)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output and Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces live local monitoring updates; Ollama layer data is available only when a readable server.log path is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
