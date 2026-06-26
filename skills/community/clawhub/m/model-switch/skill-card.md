## Description: <br>
OpenClaw one-click AI model switching skill for switching models, viewing the current model, diagnosing model issues, adding or removing models, and comparing available models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samsonvacity](https://clawhub.ai/user/samsonvacity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage OpenClaw model configuration across session state, agent defaults, allowlists, and provider authentication files. It supports model switching, provider key setup, model listing, comparison, and configuration diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change OpenClaw settings and auth profile files. <br>
Mitigation: Back up ~/.openclaw before use and review openclaw.json and auth-profiles.json after running switch, add, remove, or add-key commands. <br>
Risk: The skill can copy provider API keys from environment variables into per-agent authentication files. <br>
Mitigation: Use narrowly scoped provider keys and install only when comfortable with API keys being written into OpenClaw configuration. <br>
Risk: Bulk switching can affect all configured agents. <br>
Mitigation: Avoid switch ALL unless intentional and verify the target model and provider before executing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samsonvacity/model-switch) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Matt Pocock Skills](https://github.com/mattpocock/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw JSON configuration and per-agent auth profile files when command scripts are executed.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
