## Description: <br>
Extracts structured data from plain-text emails, including company, email address, contact person, discount code, and email type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FDrummer](https://clawhub.ai/user/FDrummer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users can provide plain-text email content and have the agent return a concise structured record for triage, categorization, or downstream data entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email content can include personal or business-sensitive information. <br>
Mitigation: Only provide email text that is appropriate for the agent to process, and review extracted JSON before using it in downstream systems. <br>


## Reference(s): <br>
- [Skill source instructions](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/FDrummer/mailparser) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [JSON object with company, email, contact_person, discount_code, and type fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email type is classified as order, offer, newsletter, or other.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
