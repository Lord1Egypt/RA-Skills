## Description: <br>
n8n (n8n.io). Use this skill for ANY n8n request -- reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage connected n8n workspaces through OOMOL, including workflow lifecycle actions, execution inspection, tags, variables, insights, and data table operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful n8n write and destructive actions through the user's connected OOMOL workspace. <br>
Mitigation: Review exact workflow, table, tag, variable, and execution targets before use, and require explicit user confirmation for write or destructive actions. <br>
Risk: The skill depends on OOMOL CLI access to a connected n8n account. <br>
Mitigation: Install and authenticate the oo CLI only when the user intends to manage n8n through OOMOL and trusts that connector path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-n8n) <br>
- [n8n homepage](https://n8n.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; write and destructive actions require confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
