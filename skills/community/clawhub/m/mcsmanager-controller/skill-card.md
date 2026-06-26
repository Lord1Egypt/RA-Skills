## Description: <br>
Control and troubleshoot MCSManager-managed Minecraft servers through the MCSManager API and clearly provided host-side context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SzaBee13](https://clawhub.ai/user/SzaBee13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Server administrators and operators use this skill to inspect, troubleshoot, and control Minecraft servers managed through MCSManager. It guides read-only checks, log review, console commands, and start, stop, restart, or kill actions when the user provides the required instance configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that use an API key to control a real MCSManager Minecraft server, including stop, kill, restart, and console-command operations. <br>
Mitigation: Use it only with an MCSManager instance the user administers, keep real config.json private and untracked, prefer least-privilege API keys, and verify the target instance before state-changing actions. <br>


## Reference(s): <br>
- [MCSManager API notes](references/api-notes.md) <br>
- [MCSManager Controller release page](https://clawhub.ai/SzaBee13/mcsmanager-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with concise operational steps, command examples, status summaries, and minimal log excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose API requests or host-side checks only from user-provided MCSManager configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
