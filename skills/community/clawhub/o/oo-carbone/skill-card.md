## Description: <br>
Carbone (carbone.io) enables agents to read, create, update, and delete Carbone data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Carbone templates from an agent through their OOMOL-connected Carbone account, including listing templates and safely managing template metadata or deletion actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent use an OOMOL-connected Carbone account. <br>
Mitigation: Install and use it only when the agent should be allowed to operate that Carbone account. <br>
Risk: Template metadata updates and template deletion actions can change or remove Carbone data. <br>
Mitigation: Require explicit user confirmation of the target, payload, and expected effect before any write or destructive action. <br>
Risk: First-time setup may involve installing the remote oo CLI. <br>
Mitigation: Allow remote CLI installation only when the user trusts the OOMOL CLI source. <br>


## Reference(s): <br>
- [Carbone homepage](https://carbone.io) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub Carbone skill page](https://clawhub.ai/oomol/skills/oo-carbone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI schema and connector-run commands; write and destructive actions require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
