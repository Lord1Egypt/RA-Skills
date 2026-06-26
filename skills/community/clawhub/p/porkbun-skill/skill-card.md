## Description: <br>
Manage Porkbun DNS records and domains via API v3, including creating, reading, updating, and deleting DNS records, listing domains, configuring API access, and working with common record types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmantly](https://clawhub.ai/user/wmantly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage Porkbun-hosted DNS records and domains through an agent using the bundled CLI. It supports API credential setup, domain and record listing, and controlled creation, editing, or deletion of common DNS record types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Porkbun API credentials are sensitive and can authorize DNS changes. <br>
Mitigation: Restrict access to environment variables or config files containing API keys, and prefer revocable credentials. <br>
Risk: Incorrect DNS edit or delete operations can disrupt websites, email delivery, or domain verification. <br>
Mitigation: Before edit-by or delete-by commands, list affected records and confirm the exact domain, record type, and record name. <br>


## Reference(s): <br>
- [DNS Record Types Reference](references/dns-record-types.md) <br>
- [Porkbun API v3 Documentation](https://porkbun.com/api/json/v3/documentation) <br>
- [Porkbun API Key Setup](https://porkbun.com/account/api) <br>
- [ClawHub Porkbun Skill Release](https://clawhub.ai/wmantly/porkbun-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a Node.js CLI that sends authenticated requests to the Porkbun API.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
