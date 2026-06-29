## Description: <br>
Salesflare helps agents read, create, and update Salesflare CRM data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and CRM operators use this skill to have an agent query Salesflare records and prepare confirmed create or update actions through OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Salesflare CRM records through OOMOL. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running any write action. <br>
Risk: CRM access is mediated through the user's OOMOL account connection. <br>
Mitigation: Install and use the skill only when Salesflare access through OOMOL is intended, and review the OOMOL CLI and Salesflare connection setup before relying on it. <br>
Risk: Read actions can return Salesflare account, contact, opportunity, task, and user data. <br>
Mitigation: Use the skill only with an authorized Salesflare connection and handle returned CRM data according to the user's access and data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub Salesflare skill](https://clawhub.ai/oomol/skills/oo-salesflare) <br>
- [Salesflare homepage](https://salesflare.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with oo CLI commands and JSON payload or response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read actions can run directly; create and update actions require confirmation of the exact payload and effect.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
