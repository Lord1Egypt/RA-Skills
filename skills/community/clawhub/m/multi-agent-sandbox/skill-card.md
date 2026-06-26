## Description: <br>
Setup multi-agent sandbox infrastructure with Docker, Discord, SSH, and Tailscale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superWorldSavior](https://clawhub.ai/user/superWorldSavior) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up sandboxed OpenClaw agents that collaborate across gateways through Discord and a shared VPS while reducing exposure of private main-agent data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Docker-to-host and VPS network bridges can expand access beyond the intended sandbox. <br>
Mitigation: Use dedicated low-privilege VPS accounts, bind bridges only to docker0, restrict firewall rules, and remove systemd bridge services when the sandbox is no longer needed. <br>
Risk: Broad agent/session permissions can expose history or allow unintended agent-to-agent actions. <br>
Mitigation: Prefer named agent allowlists over wildcards, limit session history and spawn access, and review both directions of agent permissions before use. <br>
Risk: SSH host-key bypasses and exposed Discord bot tokens can compromise the shared environment. <br>
Mitigation: Verify and pin SSH host keys, use dedicated bot accounts, keep tokens out of channels, and rotate any token that is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superWorldSavior/multi-agent-sandbox) <br>
- [Discord Developer Applications](https://discord.com/developers/applications) <br>
- [Tailscale install script](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, Dockerfile, systemd, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps for Docker sandboxing, Discord routing, socat bridges, Tailscale SSH, and agent allowlists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
