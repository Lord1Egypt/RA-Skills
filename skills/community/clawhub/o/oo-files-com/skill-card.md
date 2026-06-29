## Description: <br>
Files.com helps an agent read, create, update, and delete Files.com data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage Files.com folders, listings, file metadata, and deletions through the OOMOL files_com connector after account connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive connector actions can change or delete Files.com data. <br>
Mitigation: Confirm exact paths, payloads, and intended effects with the user before creating folders, updating metadata, or deleting files. <br>
Risk: Connector access depends on the user's OOMOL and Files.com connection scopes and credential state. <br>
Mitigation: Review the connected account scopes and resolve authentication, connection, or billing errors before retrying actions. <br>


## Reference(s): <br>
- [ClawHub Files.com Skill](https://clawhub.ai/oomol/skills/oo-files-com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Files.com Homepage](https://www.files.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent commands use the oo CLI and live action schema inspection before connector calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
