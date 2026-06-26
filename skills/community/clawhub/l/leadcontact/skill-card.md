## Description: <br>
Query verified phone numbers and email addresses from LinkedIn profile URLs using LeadContact API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhyswan](https://clawhub.ai/user/zhyswan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, recruiting, and CRM operators can use this skill to enrich LinkedIn profile URLs with phone and email data through the LeadContact API when they have a legitimate, compliant basis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can look up people's phone numbers and email addresses from LinkedIn profiles without clear consent or lawful-use guardrails. <br>
Mitigation: Use it only for legitimate, compliant enrichment workflows, avoid bulk or automated lookup without a clear legal basis, and verify outreach complies with privacy, anti-spam, and platform rules. <br>
Risk: LeadContact API tokens and returned contact data are sensitive. <br>
Mitigation: Store the API token in the platform credential store, never expose it in client-side code, and restrict access to returned contact data. <br>


## Reference(s): <br>
- [ClawHub LeadContact Listing](https://clawhub.ai/zhyswan/leadcontact) <br>
- [LeadContact Website](https://leadcontact.ai) <br>
- [LeadContact Privacy Policy](https://leadcontact.ai/zh-CN/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API request examples and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LeadContact API token and LinkedIn profile URLs as inputs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
