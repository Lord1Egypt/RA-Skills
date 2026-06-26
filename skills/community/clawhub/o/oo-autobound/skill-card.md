## Description: <br>
Autobound (autobound.ai). Use this skill for ANY Autobound request - searching and reading data. Whenever a task involves Autobound, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to query Autobound account details, signal types, company searches, contact searches, and enrichment actions through an OOMOL-connected Autobound account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Autobound credentials through an OOMOL-connected account. <br>
Mitigation: Use only with the intended OOMOL and Autobound accounts, and review connection scope or expiration errors before reconnecting. <br>
Risk: First-time setup may execute remote oo CLI installer commands. <br>
Mitigation: Review the installer URLs before running setup, and run setup only when the oo CLI is missing or authentication fails. <br>
Risk: Autobound query and enrichment payloads are sent through OOMOL and Autobound services. <br>
Mitigation: Submit only data appropriate for the connected Autobound account and inspect the live connector schema before each action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-autobound) <br>
- [Autobound Homepage](https://www.autobound.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Autobound connector schemas before action payloads; command responses may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
