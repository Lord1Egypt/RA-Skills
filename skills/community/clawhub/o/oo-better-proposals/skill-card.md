## Description: <br>
Use this Better Proposals skill for reading, creating, and updating data through a connected Better Proposals account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with a connected Better Proposals account through OOMOL, including reading account, brand, company, currency, proposal, quote, and template data and performing supported update actions when confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through a connected Better Proposals account. <br>
Mitigation: Install and use it only when you intend to let the agent access that account through OOMOL. <br>
Risk: Read and list actions may expose proposal, company, quote, template, and account settings data. <br>
Mitigation: Run actions only for authorized tasks and review returned data before sharing or persisting it. <br>
Risk: Write-tagged actions can change Better Proposals account state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any write-tagged action. <br>
Risk: CLI installer and login steps affect the local environment and account connection. <br>
Mitigation: Run setup steps only when the oo CLI or account connection is missing and the OOMOL setup is trusted. <br>


## Reference(s): <br>
- [Better Proposals](https://betterproposals.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-better-proposals) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the oo CLI and return connector JSON responses that include data and an executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
