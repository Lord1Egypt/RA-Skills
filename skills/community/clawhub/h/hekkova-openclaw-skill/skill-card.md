## Description: <br>
Permanent memory layer for AI agents. Mint moments to the blockchain via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hekkova](https://clawhub.ai/user/hekkova) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Hekkova's MCP endpoint, mint text, images, videos, and public URLs as durable moments, manage privacy phases, and export or inspect their archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected content, public URLs, and metadata may be sent to Hekkova for durable blockchain/IPFS-backed storage. <br>
Mitigation: Review sensitive data, consent, copyright, and source metadata before minting. <br>
Risk: Minting, phase changes, and video actions can consume Hekkova credits and may create publication-like records. <br>
Mitigation: Require manual approval for mint_moment, mint_from_url, and update_phase to full_moon, and check credit balance before paid actions. <br>
Risk: Changing a moment to full_moon makes it fully public with no encryption. <br>
Mitigation: Confirm the target Block ID and public-release intent before updating a moment to full_moon. <br>
Risk: HEKKOVA_API_KEY grants access to the user's Hekkova account. <br>
Mitigation: Keep the API key private and avoid storing or logging it in agent output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hekkova/hekkova-openclaw-skill) <br>
- [Hekkova Homepage](https://hekkova.com) <br>
- [Hekkova App](https://app.hekkova.com) <br>
- [Hekkova MCP Endpoint](https://mcp.hekkova.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP connection commands, tool usage notes, and returned Hekkova identifiers or archive data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Block IDs, Token IDs, privacy phases, credit balances, IPFS CIDs, Filecoin status, wallet details, and Polygon transaction URLs returned by Hekkova tools.] <br>

## Skill Version(s): <br>
1.2.1 (source: server evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
