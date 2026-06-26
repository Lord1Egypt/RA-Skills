## Description: <br>
Jobber API integration with managed OAuth for managing clients, jobs, invoices, quotes, properties, and team members for field service businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Jobber through Maton-managed OAuth for reading and managing clients, jobs, invoices, quotes, properties, requests, and team members. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY and the connected OAuth account can provide access to sensitive Jobber business records. <br>
Mitigation: Install only when the publisher and Maton brokered access are trusted, keep the API key out of shared logs, and scope access through the intended Jobber connection. <br>
Risk: Create, update, or delete operations can change clients, jobs, invoices, quotes, schedules, or other business records. <br>
Mitigation: Require explicit user approval before every write operation and confirm the target resource, account connection, and intended effect. <br>
Risk: Multiple active Jobber connections can route requests to the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one connection exists and verify the selected connection before executing actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/jobber) <br>
- [Jobber Developer Documentation](https://developer.getjobber.com/docs/) <br>
- [Jobber Getting Started Guide](https://developer.getjobber.com/docs/getting_started/) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a valid Jobber OAuth connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
