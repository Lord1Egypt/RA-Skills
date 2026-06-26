## Description: <br>
Habitica (habitica.com) support for reading, creating, updating, deleting, and scoring Habitica user data through the OOMOL Habitica connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate their connected Habitica account for profile, task, tag, scoring, and task-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Habitica account and depends on OOMOL-mediated account access. <br>
Mitigation: Install it only when the user wants an agent to operate that Habitica account through OOMOL and trusts the account connection. <br>
Risk: Write actions can create, update, or score Habitica tasks and tags. <br>
Mitigation: Confirm the exact action, payload, and expected account effect with the user before running write actions. <br>
Risk: Destructive actions can delete Habitica tasks or tags. <br>
Mitigation: Require explicit approval for the target task or tag before deletion. <br>


## Reference(s): <br>
- [ClawHub Habitica skill page](https://clawhub.ai/oomol/oo-habitica) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Habitica homepage](https://habitica.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Habitica connector action names, payload descriptions, and returned JSON summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
