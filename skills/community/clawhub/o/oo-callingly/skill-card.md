## Description: <br>
Callingly (callingly.com). Use this skill for ANY Callingly request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent operate Callingly through an OOMOL-connected account, including reading calls, leads, teams, agents, and schedules, plus creating calls and updating or deleting leads when confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create calls or update Callingly lead data. <br>
Mitigation: Confirm the exact action payload and expected effect with the user before running write actions. <br>
Risk: The destructive delete_lead action can remove Callingly lead data. <br>
Mitigation: Require explicit approval for the target lead before running deletion. <br>
Risk: First-time setup may require installing or authenticating the oo CLI. <br>
Mitigation: Review the oo CLI install method before setup and only run authentication or connection steps after a command fails for the matching reason. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-callingly) <br>
- [Callingly Homepage](https://callingly.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent fetches the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
