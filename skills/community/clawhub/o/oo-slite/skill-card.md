## Description: <br>
Operates Slite through an OOMOL-connected account to read, create, update, delete, list, and search Slite notes and groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a connected Slite workspace through the oo CLI for reading, searching, creating, updating, and deleting notes and groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Slite workspace content through an OOMOL-connected account. <br>
Mitigation: Confirm exact note targets, payloads, and effects before write actions, and require explicit approval before destructive delete actions. <br>
Risk: The skill depends on connected Slite credentials and the scopes granted to the OOMOL connector. <br>
Mitigation: Review the connected Slite API key scopes before installation or use. <br>
Risk: The optional oo CLI installer runs a remote install script. <br>
Mitigation: Run the installer only when the CLI is missing and only after trusting OOMOL's installer source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-slite) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Slite Homepage](https://slite.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live Slite connector schema inspection before action execution; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
