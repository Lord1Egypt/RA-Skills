## Description: <br>
Keap API integration with managed OAuth for managing contacts, companies, tags, tasks, orders, opportunities, and campaigns in CRM and marketing automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to access Keap CRM data and perform managed CRM and marketing automation actions through Maton OAuth connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad Keap CRM account access through Maton, including contacts, companies, tags, tasks, orders, opportunities, campaigns, and email operations. <br>
Mitigation: Install only when Maton-mediated Keap access is intended; protect MATON_API_KEY and verify the target Keap connection before use. <br>
Risk: Write operations can create, update, delete, send, or modify CRM and marketing automation resources. <br>
Mitigation: Require explicit user approval and confirm the target resource and intended effect before any write action. <br>
Risk: Multiple Keap OAuth connections can cause actions to run against the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one Keap connection exists. <br>


## Reference(s): <br>
- [ClawHub Keap skill page](https://clawhub.ai/byungkyu/keap) <br>
- [Keap Developer Portal](https://developer.infusionsoft.com/) <br>
- [Keap REST API V2 Documentation](https://developer.infusionsoft.com/docs/restv2/) <br>
- [Keap Getting Started Guide](https://developer.infusionsoft.com/getting-started/) <br>
- [Keap OAuth 2.0 Authentication](https://developer.infusionsoft.com/authentication/) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Keap OAuth account; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata); SKILL.md frontmatter lists 1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
