## Description:

Watches NVIDIA GPU and local Ollama health for always-on boxes and GPU earning workers — checks Ollama API, GPU util and VRAM via nvidia-smi, auto-restarts Ollama on failure, appends JSON status logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wq920809](https://clawhub.ai/user/wq920809)

### License/Terms of Use:

MIT-0

## Use Case:

Windows operators and developers running always-on local Ollama workloads use this skill to check the Ollama API and NVIDIA GPU status, log health data, and optionally start Ollama after an API failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled checks continue until the Windows task is removed, and status logs accumulate locally.

Mitigation: Start with -NoHeal to observe behavior, remove the scheduled task when it is no longer needed, and manage the local log file.

Risk: The advertised HealCommand parameter is unused; recovery always attempts to start Ollama with 'serve'.

Mitigation: Review the recovery behavior and confirm that starting Ollama with 'serve' is appropriate before enabling healing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wq920809/skills/gpu-ollama-sentinel)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [PowerShell script, Markdown usage guidance, and JSONL status logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The watchdog appends one JSON record per check to a local JSONL log.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
