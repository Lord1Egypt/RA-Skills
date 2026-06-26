## Description: <br>
Helps OpenClaw users connect multiple OpenClaw instances for API communication, SSH file transfer, and scheduled memory synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milkteawithsoybeanmilktast](https://clawhub.ai/user/milkteawithsoybeanmilktast) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up communication, file transfer, and memory sharing across trusted OpenClaw instances running on different machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-machine OpenClaw control can expose powerful API tokens, SSH keys, hosts, and remote execution paths. <br>
Mitigation: Use only instances you control and trust; prefer private networking, scoped credentials, protected SSH keys, and explicit review of hosts and tokens before setup. <br>
Risk: Memory and tool-file synchronization can copy sensitive identity, memory, or secret-bearing files between machines. <br>
Mitigation: Review every file selected for sync, avoid syncing TOOLS.md or other secret-bearing files unless manually checked, and keep backups before synchronization. <br>
Risk: Scheduled synchronization can repeatedly propagate mistakes or unwanted changes across instances. <br>
Mitigation: Require explicit confirmation before enabling cron jobs, restrict sync paths, and inspect synchronization reports after each run. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/milkteawithsoybeanmilktast/openclaw-multi-instance) <br>
- [Peer configuration template](references/peer-config.json5) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON5, cron, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to configure remote API access, SSH transfer, cron jobs, and memory synchronization files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
