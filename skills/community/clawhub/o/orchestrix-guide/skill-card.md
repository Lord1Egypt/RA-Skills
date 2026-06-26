## Description: <br>
Orchestrix multi-agent workflow guide for OpenClaw, covering planning, development, tmux command protocol, task completion detection, and supplementary bug fix, iteration, brownfield, and change-management flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorayo](https://clawhub.ai/user/dorayo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this guide to coordinate Orchestrix agents through tmux and Claude Code across planning, development, testing, bug fix, iteration, and brownfield workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes hands-off coding automation while bypassing Claude Code safety prompts. <br>
Mitigation: Remove the skipped-permissions alias, keep Claude Code approvals and folder trust prompts manual, and monitor tmux sessions while workflows run. <br>
Risk: Project-local .orchestrix-core scripts may execute automation that changes files or routes agent work. <br>
Mitigation: Inspect .orchestrix-core scripts in the target project before use and review generated changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorayo/orchestrix-guide) <br>
- [Orchestrix MCP homepage](https://orchestrix-mcp.youlidao.ai) <br>
- [Claude Code download](https://claude.ai/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with shell command examples and workflow tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only operational guide for macOS and Linux environments using OpenClaw, tmux, Claude Code, and Orchestrix project scripts.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
