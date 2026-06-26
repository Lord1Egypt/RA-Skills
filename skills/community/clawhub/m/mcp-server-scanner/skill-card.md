## Description: <br>
Scans and assesses MCP servers for vulnerabilities, insecure configurations, data exposure, and compliance with SOC 2, GDPR, and ISO 27001 standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, developers, and platform engineers use this skill to inventory authorized MCP servers, assess security posture, identify data exposure, and produce remediation and compliance guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized scanning could inspect MCP environments outside the user's authority. <br>
Mitigation: Install or invoke the skill only for MCP environments the user owns or is authorized to assess, and define the in-scope paths, accounts, and servers before use. <br>
Risk: Generated inventories and findings can expose sensitive server URLs, credential locations, or PII/SPII exposure details. <br>
Mitigation: Treat generated scan reports as sensitive security artifacts and restrict storage, sharing, and retention accordingly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/engsathiago/mcp-server-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance, Configuration] <br>
**Output Format:** [Markdown reports with inventories, severity-scored findings, remediation steps, and compliance status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive server inventory, credential-location, URL, and PII/SPII exposure details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact/package.json, artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
