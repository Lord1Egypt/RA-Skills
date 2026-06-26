## Description: <br>
MCP Colombia Hub aggregates Colombian services through an MCP server for MercadoLibre product search, Booking.com hotel search, flight references, Colombian financial-product comparisons, job applications, and Soulprint identity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ManuelFelipeArias](https://clawhub.ai/user/ManuelFelipeArias) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to configure and operate an MCP-compatible Colombian services hub for product, travel, finance, job-search, and identity-verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process Soulprint tokens, DID or reputation data, CV or LinkedIn URLs, salary expectations, and cover messages. <br>
Mitigation: Treat these values as sensitive, avoid logging or sharing them unnecessarily, and require explicit user confirmation before job-application use. <br>
Risk: The MCP server is installed and run through an external npm package. <br>
Mitigation: Install only from trusted environments and review the package and requested capabilities before enabling it in an MCP client. <br>
Risk: Real-time search features may send travel, job, or identity-related context to third-party services. <br>
Mitigation: Disclose the involved services to users and confirm consent before sending personal or job-application data. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ManuelFelipeArias/mcp-colombia) <br>
- [mcp-colombia-hub npm package](https://www.npmjs.com/package/mcp-colombia-hub) <br>
- [Soulprint validator node](https://soulprint-node-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Text] <br>
**Output Format:** [Markdown with JSON and bash code blocks plus MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npx; real-time job and travel search may require BRAVE_API_KEY; some operations use Soulprint identity tokens.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
