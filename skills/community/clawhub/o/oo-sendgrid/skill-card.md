## Description: <br>
This skill helps agents read, create, and update SendGrid data through an OOMOL-connected SendGrid account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect SendGrid account details, list transactional templates, check user scopes, and send transactional email through an OOMOL-connected SendGrid account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may operate a SendGrid account using sensitive connected credentials. <br>
Mitigation: Install only if the user trusts OOMOL and wants this connector to operate the linked SendGrid service. <br>
Risk: The optional first-time setup path includes remote installer commands. <br>
Mitigation: Prefer official installation documentation or verify the installer before running remote scripts in a shell. <br>
Risk: The send_email action changes external service state by sending transactional email. <br>
Mitigation: Confirm the exact payload and effect with the user before running write actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-sendgrid) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [SendGrid Homepage](https://sendgrid.com) <br>
- [SendGrid Connection Setup](https://console.oomol.com/app-connections?provider=sendgrid) <br>
- [SendGrid Icon](https://static.oomol.com/logo/third-party/SendGrid.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute oo CLI connector actions that return JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
