## Description: <br>
MaintainX (getmaintainx.com). Use this skill for any MaintainX request, including reading, creating, updating, and deleting data through the OOMOL MaintainX connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent retrieve and manage MaintainX locations, users, work orders, comments, and work order status through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change MaintainX data, including records, users, work order status, comments, and locations. <br>
Mitigation: Require explicit user confirmation before write actions and destructive actions, including the exact target, payload, and expected effect. <br>
Risk: The skill operates a MaintainX account through OOMOL. <br>
Mitigation: Install it only for users who intend agent-operated MaintainX access through OOMOL, and review the oo CLI installation and OOMOL connection steps before approving setup. <br>


## Reference(s): <br>
- [ClawHub MaintainX skill page](https://clawhub.ai/oomol/skills/oo-maintainx) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [MaintainX homepage](https://www.getmaintainx.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running MaintainX actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
