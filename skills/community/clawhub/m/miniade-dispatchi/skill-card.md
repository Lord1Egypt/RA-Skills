## Description: <br>
Launch non-blocking interactive Claude Code tasks for slash-only plugins like ralph-loop when a task needs interactive slash commands and completion callback routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edxi](https://clawhub.ai/user/edxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Dispatchi to start background interactive Claude Code tasks for slash-command workflows such as ralph-loop and to route completion output without blocking the caller. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts background Claude Code sessions in local repositories. <br>
Mitigation: Install only when this behavior is expected, use simple safe project and task names, and run it only in repositories where background agent activity is acceptable. <br>
Risk: The security summary flags auto-accepted safety prompts and weak validation of user-controlled paths and prompts. <br>
Mitigation: Avoid bypassPermissions or broad permission modes, review prompts before dispatch, and prefer a version that validates paths, fixes shell quoting, and stops auto-accepting Claude safety prompts. <br>
Risk: Optional callback routing can send completion information outside the local process. <br>
Mitigation: Keep callbacks disabled unless needed and enable them only with explicit group settings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edxi/miniade-dispatchi) <br>
- [Claude Code headless documentation](https://code.claude.com/docs/en/headless) <br>
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text status output with shell command execution and local configuration behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts a background tmux-backed Claude Code session, writes task metadata and output to configured local result paths, and can enable callbacks only when configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
