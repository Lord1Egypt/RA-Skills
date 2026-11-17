## Description: <br>
DNS管理入门工具 helps developers and small website operators manage Namecheap DNS records, including creating, querying, updating, deleting, and exporting common record types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, site operators, and automation agents use this skill to configure Namecheap DNS records for personal domains and small websites. It supports common DNS tasks such as listing domains, adding or updating A/CNAME/MX/TXT records, exporting records, checking propagation, and changing nameservers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broad agent powers and loosely scoped activation for DNS management. <br>
Mitigation: Review the skill before installation and use it only for explicit Namecheap DNS tasks. <br>
Risk: The security summary flags destructive DNS examples, including update, delete, and nameserver operations without clear safeguards. <br>
Mitigation: Export current DNS records before changes and require explicit confirmation before update, delete, or nameserver operations. <br>
Risk: The security guidance calls out protected Namecheap API credentials for important domains. <br>
Mitigation: Keep Namecheap API credentials scoped and protected, and verify ClientIP restrictions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/namecheap-dns-tool-free) <br>
- [Namecheap API endpoint](https://api.namecheap.com/xml.response) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured responses may include status, result data, execution logs, execution time, metadata, and error details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
