## Description: <br>
BoloForms connector skill for reading, creating, and updating BoloForms data through an OOMOL-connected account via the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect BoloForms documents, retrieve form responses, review template respondents, and send existing templates for signing through an authenticated OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected BoloForms account and can access workspace documents, form responses, and signing participant data. <br>
Mitigation: Install it only for users who intend to let the oo CLI access their BoloForms workspace, and keep the OOMOL connection scoped to the needed account. <br>
Risk: The send_template_for_signing action changes BoloForms state by sending an existing template for signing. <br>
Mitigation: Review the exact payload and expected effect with the user before approving the write action. <br>
Risk: First-time setup may use remote installer commands for the oo CLI. <br>
Mitigation: Use the remote installer commands only when the CLI is missing and the OOMOL CLI source is trusted. <br>


## Reference(s): <br>
- [BoloForms homepage](https://www.boloforms.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-boloforms) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, a signed-in OOMOL account, and a connected BoloForms workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
