## Description: <br>
Ora决策人开发专家 helps users look up company profiles and decision-maker contact details by company name, domain, or LinkedIn company identifier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oraagent](https://clawhub.ai/user/oraagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales and business-development users use this skill to retrieve company details, public contact channels, and decision-maker contact records for lawful B2B prospecting. The skill supports lookups by company name, company domain, or LinkedIn company identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup targets and the OraAgent API key are sent to api.topeasychina.com during searches. <br>
Mitigation: Use the skill only when that external transmission is acceptable, avoid internal or private domains, and restrict use to lawful business-contact lookups. <br>
Risk: Raw returned company and contact data is saved as JSON files in the working directory. <br>
Mitigation: Delete result files when no longer needed and avoid retaining unnecessary personal or sensitive contact data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oraagent/ora-contact-pro) <br>
- [OraAgent publisher profile](https://clawhub.ai/user/oraagent) <br>
- [OraAgent platform](https://www.oraskl.com/platform) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON files, guidance] <br>
**Output Format:** [Markdown summary of company and contact data, with raw JSON result files written by the selected Node.js lookup script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads OraAgent.key for API authorization and writes raw returned contact data as JSON files in the working directory.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
