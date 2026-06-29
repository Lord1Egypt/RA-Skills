## Description: <br>
IPFS Content Gateway fetches content from IPFS by CID with automatic gateway failover, uploads files up to 10MB with pinning, and lists upload history through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve IPFS content by CID, upload base64-encoded files for pinning, and review prior uploads through AgentPMT remote calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded IPFS files may be reachable by anyone who obtains the CID or gateway URL and may remain available after tool use. <br>
Mitigation: Do not upload private, regulated, or secret material unless it is encrypted first. <br>
Risk: Optional pinning service API keys are sensitive credentials. <br>
Mitigation: Pass pinning API keys only through trusted secret-handling paths and avoid placing them in prompts or logs. <br>
Risk: Shared pinning infrastructure may have usage limits or persistence characteristics outside the caller's direct control. <br>
Mitigation: Use caller-owned Pinata, Web3.Storage, or NFT.Storage credentials for heavier or business-critical usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/ipfs-content-gateway) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/ipfs-content-gateway) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines list, retrieve, and upload actions; uploads require base64 content and are limited to 10MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
