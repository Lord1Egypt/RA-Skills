## Description: <br>
This skill helps agents manage remote SSH servers through MCP ssh-manager workflows for command execution, sessions, file transfer, monitoring, tunneling, backups, and workdir-based operation records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iMaxTomas](https://clawhub.ai/user/iMaxTomas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to run, document, and compare SSH-based server operations such as deployments, health checks, troubleshooting, file transfer, tunnels, and backups. It is intended for trusted hosts where the operator can review high-impact remote actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad SSH administration actions on remote hosts, including sudo commands, service restarts, tunnels, syncs, backups, restores, and session closure. <br>
Mitigation: Install only for trusted hosts, use least-privilege SSH accounts, and require operator confirmation before high-impact actions such as sudo, sync, restore, tunnel, service restart, and session-closing operations. <br>
Risk: Workdir logs, status snapshots, summaries, and command outputs may contain sensitive infrastructure details. <br>
Mitigation: Protect saved workdir outputs with restrictive permissions, redact sensitive data before sharing, and clean up records when they are no longer needed. <br>
Risk: Long-lived SSH sessions and tunnels can persist beyond the immediate task if not closed. <br>
Mitigation: List active sessions and tunnels before and after work, reuse only relevant sessions, and explicitly close sessions and tunnels when the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iMaxTomas/mcp-ssh-manager) <br>
- [Session management deep dive](references/sessions.md) <br>
- [Workdir structure and usage](references/workspace.md) <br>
- [Comparing historical data](references/comparison.md) <br>
- [System check workflow example](examples/system-check.md) <br>
- [Multi-step deployment workflow example](examples/deployment.md) <br>
- [Troubleshooting workflow example](examples/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool calls, JSON snippets, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local workdir records containing command logs, status snapshots, summaries, and captured SSH outputs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
