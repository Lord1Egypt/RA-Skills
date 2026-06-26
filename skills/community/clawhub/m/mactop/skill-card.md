## Description: <br>
Retrieve real-time hardware metrics from Apple Silicon Macs using mactop's TOON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metaspartan](https://clawhub.ai/user/metaspartan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and Mac operators use this skill to collect and summarize local Apple Silicon hardware metrics such as CPU, memory, GPU, power, thermal state, network, disk I/O, and Thunderbolt information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Homebrew mactop package and local Apple Silicon hardware metric availability. <br>
Mitigation: Install mactop with Homebrew only from a trusted package source and verify it is available before running metric commands. <br>
Risk: The agent may run local hardware monitoring commands on the user's Mac. <br>
Mitigation: Review commands before execution and limit use to read-only mactop invocations for hardware metrics. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and readable metric summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local read-only mactop hardware monitoring output in TOON format.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
