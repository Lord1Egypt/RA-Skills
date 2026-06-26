## Description: <br>
Send real handwritten notes through robots with real pens - physical cards mailed to recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidwachs](https://clawhub.ai/user/davidwachs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to let an AI assistant browse Handwrytten card options, prepare handwritten-card orders, manage address-book assets, and send single or bulk physical mail after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place paid physical-mail orders, including bulk sends and basket submissions. <br>
Mitigation: Require explicit human confirmation of the card, font, message, recipients, sender, extras, schedule, and cost before send_order or basket_send. <br>
Risk: The Handwrytten API key authorizes account actions and account data access. <br>
Mitigation: Use a dedicated or revocable API key if available, keep it out of chat, and configure it only as HANDWRYTTEN_API_KEY in the client environment. <br>
Risk: The skill can create, update, delete, or upload account assets such as recipients, senders, QR codes, images, and custom cards. <br>
Mitigation: Review destructive or asset-changing operations before execution and confirm uploads use intended public image URLs. <br>


## Reference(s): <br>
- [Handwrytten MCP Server](https://github.com/handwrytten/handwrytten-mcp-server) <br>
- [Handwrytten API](https://www.handwrytten.com/api/) <br>
- [Handwrytten](https://www.handwrytten.com) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Text and JSON returned by MCP tools, with configuration snippets for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and HANDWRYTTEN_API_KEY; tool actions can create paid physical-mail orders and modify Handwrytten account assets.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact package.json and MCP server report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
