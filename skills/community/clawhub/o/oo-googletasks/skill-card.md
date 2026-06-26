## Description: <br>
Google Tasks (tasks.google.com). Use this skill for ANY Google Tasks request: reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Google Tasks through an OOMOL-connected account, including listing, fetching, creating, updating, moving, clearing, and deleting tasks and task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create, update, or move Google Tasks data. <br>
Mitigation: Confirm the exact action payload and expected effect before approving write actions. <br>
Risk: Destructive actions can clear completed tasks or delete tasks and task lists. <br>
Mitigation: Require explicit approval for the target task list or task before running destructive actions. <br>
Risk: Incorrect connector payloads can affect the wrong Google Tasks item. <br>
Mitigation: Inspect the live connector schema before building each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-googletasks) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Google Tasks](https://tasks.google.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may return JSON data and an execution ID from the OOMOL connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
