## Description: <br>
Find ICP-matching exhibitors, prospects, and partners at any trade show using the Lensmor API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B sales and marketing teams use this skill to find trade-show exhibitors, prospects, partners, or competitors that match a company URL or target-audience profile before an event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided company URLs, event identifiers, and target-audience descriptions are sent to Lensmor as part of the exhibitor search workflow. <br>
Mitigation: Avoid entering confidential strategy, private customer lists, credentials, or internal documents, and use only inputs appropriate to share with Lensmor. <br>
Risk: The skill depends on a Lensmor API key for external exhibitor data access. <br>
Mitigation: Store LENSMOR_API_KEY securely, never disclose it in responses, and verify that the key is configured before making API calls. <br>


## Reference(s): <br>
- [Lensmor API documentation](https://api.lensmor.com/) <br>
- [Lensmor platform](https://platform.lensmor.com) <br>
- [ClawHub release page](https://clawhub.ai/weilun88313/lensmor-exhibitor-search) <br>
- [Example: SaaS vendor prospecting at Dreamforce 2026](examples/saas-vendor-at-dreamforce.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured exhibitor tables, ICP match notes, error messages, and concise follow-up suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; returns paginated exhibitor search results grounded in Lensmor API response fields.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
