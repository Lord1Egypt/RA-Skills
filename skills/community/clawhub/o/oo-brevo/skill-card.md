## Description: <br>
Brevo lets an agent read, create, update, and delete Brevo data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage Brevo account, contact, contact-list, and folder workflows through an OOMOL-connected Brevo account. It supports read actions directly and requires confirmation before write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a Brevo account through OOMOL and may require sensitive account connections or scopes. <br>
Mitigation: Connect only the Brevo account and scopes intended for agent use, and rely on OOMOL server-side credential injection rather than handling raw tokens. <br>
Risk: Installer commands fetch and execute the oo CLI installer from a remote URL. <br>
Mitigation: Review the oo CLI installer before running it, and run setup only when the CLI is missing. <br>
Risk: Write and destructive actions can create, update, delete, or remove Brevo contact and list data. <br>
Mitigation: Inspect the live action schema before building payloads, confirm write payloads and effects with the user, and require explicit approval for destructive actions. <br>


## Reference(s): <br>
- [ClawHub Brevo skill](https://clawhub.ai/oomol/oo-brevo) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Brevo homepage](https://www.brevo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return JSON data with execution metadata; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
