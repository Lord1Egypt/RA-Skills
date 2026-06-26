## Description: <br>
Manage Hostinger account via API - VPS administration, snapshots, backups, firewall, Docker, DNS zone management, domain portfolio, website hosting, and billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexlunae](https://clawhub.ai/user/rexlunae) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Hostinger infrastructure and account resources through Hostinger API commands, including VPS operations, DNS updates, Docker deployments, domain settings, hosting inventory, and billing views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over production Hostinger resources, including disruptive VPS, DNS, firewall, billing, and Docker operations. <br>
Mitigation: Use the least-privileged Hostinger API token available, protect and rotate it, and require explicit human approval before executing reset, restore, recreate, delete, nameserver, root-password, SSH-key, firewall, billing, or Docker deploy commands. <br>
Risk: Docker deployment from an external compose URL can introduce unreviewed workload definitions into managed infrastructure. <br>
Mitigation: Review compose files and source URLs before deployment, especially when the compose file or URL comes from outside your control. <br>


## Reference(s): <br>
- [Hostinger API Reference](references/api-endpoints.md) <br>
- [Hostinger API Documentation](https://developers.hostinger.com) <br>
- [Hostinger OpenAPI Specification](https://github.com/hostinger/api/blob/main/openapi.json) <br>
- [Hostinger Python SDK](https://github.com/hostinger/api-python-sdk) <br>
- [Hostinger API CLI](https://github.com/hostinger/api-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled CLI prints Hostinger API responses as formatted JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
