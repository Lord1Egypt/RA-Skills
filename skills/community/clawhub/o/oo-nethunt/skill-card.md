## Description: <br>
NetHunt helps an agent read, create, update, and delete NetHunt CRM data through OOMOL's oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to let an agent inspect NetHunt schemas, run read actions, and perform approved record, comment, and call-log mutations through an OOMOL-connected NetHunt account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read actions may expose NetHunt CRM data. <br>
Mitigation: Install and use the skill only for intended CRM access, and review returned data before sharing it outside the authorized context. <br>
Risk: Write and delete actions can change or remove business records. <br>
Mitigation: Confirm the exact payload, target record, and expected effect with the user before running any write or destructive action. <br>
Risk: The one-time CLI install command runs OOMOL's remote installer. <br>
Mitigation: Run the installer only when the oo CLI is required and the user trusts OOMOL's installer source. <br>


## Reference(s): <br>
- [ClawHub NetHunt skill page](https://clawhub.ai/oomol/skills/oo-nethunt) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [NetHunt homepage](https://nethunt.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands typically return JSON from the oo CLI; write and destructive actions require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
