## Description: <br>
Finds a LinkedIn profile URL for an Odoo contact using their name and company, then saves it to the x_linkedin_url field in Odoo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernhmueller](https://clawhub.ai/user/bernhmueller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and CRM administrators use this skill to enrich Odoo contacts by finding a likely LinkedIn profile URL from the contact name and company, then writing it to the contact's x_linkedin_url field. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends CRM contact names and company names to DuckDuckGo while searching for LinkedIn profile candidates. <br>
Mitigation: Install only when organizational policy allows this data sharing for contact enrichment. <br>
Risk: The skill can overwrite the x_linkedin_url field on an Odoo contact. <br>
Mitigation: Use a least-privileged Odoo API key limited to required contact read/write access and run the script only for intended contact IDs. <br>
Risk: Search results may identify the wrong LinkedIn profile for a contact. <br>
Mitigation: Manually verify the found LinkedIn URL before relying on the updated CRM field. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernhmueller/linkedin-odoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Plain text terminal output from a Python script, with Odoo contact updates performed through XML-RPC.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Odoo connection credentials from environment variables and one Odoo contact ID argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
