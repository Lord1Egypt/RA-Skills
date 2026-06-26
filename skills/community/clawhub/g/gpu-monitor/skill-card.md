## Description: <br>
Provides real-time NVIDIA GPU usage and memory stats, plus Ollama model layer GPU/CPU distribution via server.log parsing with live updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinkerjueberg](https://clawhub.ai/user/tinkerjueberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor local NVIDIA GPU memory, utilization, and temperature while running Ollama workloads, including GPU versus CPU model layer placement when Ollama server logs are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local GPU inspection commands and may read an Ollama server log path supplied by the user. <br>
Mitigation: Run it only on systems where local GPU telemetry is expected, and provide only Ollama log paths that the agent is authorized to read. <br>
Risk: The monitor runs continuously until interrupted. <br>
Mitigation: Use an appropriate refresh interval and stop the process when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinkerjueberg/gpu-monitor) <br>
- [Ollama framework](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Terminal text output with optional JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Continuously refreshed local status output; default interval is 2 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
