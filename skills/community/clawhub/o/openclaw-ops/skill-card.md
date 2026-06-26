## Description: <br>
Use when diagnosing, repairing, or maintaining an OpenClaw Gateway on the same machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinstein](https://clawhub.ai/user/dinstein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill with a trusted rescue agent to diagnose, repair, update, back up, and health-check an OpenClaw Gateway on Linux or macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide a trusted agent to access OpenClaw configuration, session data, environment files, tokens, and backups. <br>
Mitigation: Install it only on a trusted rescue or operations agent, avoid printing secrets, and protect backup directories because they may contain credentials. <br>
Risk: Maintenance guidance can include service restarts, package updates, transcript cleanup, and Tailscale Serve resets. <br>
Mitigation: Review commands before approval, require explicit confirmation for destructive operations, create backups before modifying configuration, and verify service health after changes. <br>


## Reference(s): <br>
- [ClawHub OpenClaw Ops listing](https://clawhub.ai/dinstein/openclaw-ops) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires same-machine shell access and review before privileged or destructive operations.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
