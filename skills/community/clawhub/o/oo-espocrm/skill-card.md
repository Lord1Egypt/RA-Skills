## Description: <br>
EspoCRM (espocrm.com). Use this skill for ANY EspoCRM request: reading, creating, updating, and deleting data through an OOMOL-connected EspoCRM account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to read EspoCRM users, metadata, records, and record lists, and to create, update, or delete CRM records through the OOMOL oo CLI connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive EspoCRM account data through the connected OOMOL account. <br>
Mitigation: Install it only when OOMOL is trusted with EspoCRM access and run it under an account with appropriate CRM permissions. <br>
Risk: Write and delete actions can change or remove real CRM records. <br>
Mitigation: Review the exact payload and intended effect before approving create, update, or delete actions. <br>


## Reference(s): <br>
- [EspoCRM homepage](https://www.espocrm.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-espocrm) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents inspect the live EspoCRM action schema before constructing connector payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
