## Description: <br>
ActiveCampaign (activecampaign.com). Use this skill for ANY ActiveCampaign request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with ActiveCampaign through an OOMOL-connected account, including reading users, contacts, fields, and mailing lists, and creating or updating contacts when confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected account and can access ActiveCampaign CRM data. <br>
Mitigation: Enable it only where ActiveCampaign access is intended and use the least-privilege account or connection available. <br>
Risk: The upsert_contact action can create or update ActiveCampaign contacts. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The authoritative security guidance says the disclosed commands should be used deliberately. <br>
Mitigation: Review command targets and requested changes before execution, and keep credential scope limited. <br>


## Reference(s): <br>
- [ActiveCampaign homepage](https://www.activecampaign.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL ActiveCampaign connection](https://console.oomol.com/app-connections?provider=activecampaign) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-activecampaign) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs the agent to inspect live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
