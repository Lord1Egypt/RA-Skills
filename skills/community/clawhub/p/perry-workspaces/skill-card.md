## Description: <br>
Create and manage isolated Docker workspaces on your tailnet with Claude Code and OpenCode pre-installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gricha](https://clawhub.ai/user/gricha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a compact command reference for creating, listing, stopping, deleting, shelling into, and connecting to Perry Docker workspaces on a tailnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents powerful workspace lifecycle commands that can create, stop, delete, or open shells into development containers. <br>
Mitigation: Review workspace names before execution and confirm destructive commands such as `perry remove <name>` before running them. <br>
Risk: SSH and tailnet connection guidance may connect an agent to a remote workspace. <br>
Mitigation: Verify the target workspace hostname or IP address and use the documented `workspace` user when connecting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gricha/perry-workspaces) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Perry, SSH, Tailscale, Claude Code, and OpenCode command guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
