## Description: <br>
Permanent memory layer for AI agents. Mint moments to the blockchain via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hekkova](https://clawhub.ai/user/hekkova) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Hekkova to connect an agent to Hekkova's MCP service, mint text, image, video, and URL-based moments to Polygon/IPFS, manage privacy phases, check credits, and export archived moments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to a paid permanent-memory service where minting, URL minting, and phase changes may be billable and difficult to undo. <br>
Mitigation: Check balance before paid actions, confirm user intent before minting or changing phases, and report remaining credits after successful mints. <br>
Risk: Minted content may become permanent, public, or externally accessible when privacy phases or source URLs are chosen incorrectly. <br>
Mitigation: Default to the encrypted owner-only phase, avoid minting secrets, credentials, regulated personal data, private URLs, or third-party content without permission, and require explicit confirmation before using public phases. <br>
Risk: The connection uses a remote MCP bridge and a Hekkova API key. <br>
Mitigation: Use a dedicated API key with limited credits, pass it only through the HEKKOVA_API_KEY environment variable, and do not store or print the key in agent outputs. <br>


## Reference(s): <br>
- [ClawHub Hekkova skill page](https://clawhub.ai/hekkova/hekkova) <br>
- [Hekkova homepage](https://hekkova.com) <br>
- [Hekkova app dashboard](https://app.hekkova.com) <br>
- [Hekkova MCP endpoint](https://mcp.hekkova.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and HEKKOVA_API_KEY; minting, URL minting, and phase changes may consume Hekkova credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata.openclaw.version is 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
