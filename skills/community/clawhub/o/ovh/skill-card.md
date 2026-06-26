## Description: <br>
Manage OVHcloud services via API for OVH domains, DNS records, VPS, cloud instances, dedicated servers, email, SSL certificates, and service management tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushp1997](https://clawhub.ai/user/pushp1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer OVHcloud resources through an agent-assisted CLI workflow, including account lookup, DNS changes, server lifecycle actions, cloud instance inspection, SSL certificate listing, and billing or order review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete DNS records and refresh zones. <br>
Mitigation: Require explicit human confirmation before DNS create, update, delete, or refresh operations, and review the target domain, record ID, record type, and target value before execution. <br>
Risk: The skill can stop, start, or reboot VPS and dedicated server resources. <br>
Mitigation: Use least-privilege OVH API credentials and require human approval before lifecycle actions that can disrupt running services. <br>
Risk: The skill can read account, order, and billing information. <br>
Mitigation: Treat CLI output as sensitive, avoid exposing billing results in shared logs, and scope credentials away from accounts or projects the agent does not need. <br>


## Reference(s): <br>
- [OVH API token creation](https://ca.api.ovh.com/createToken/) <br>
- [ClawHub skill page](https://clawhub.ai/pushp1997/ovh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read account and billing data and may trigger OVHcloud resource changes through authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
