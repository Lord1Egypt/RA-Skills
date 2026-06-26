## Description: <br>
Creates Guoguo courier shipment orders through an MCP-connected service after collecting sender, receiver, address, account, and pickup-time details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dazhanggui](https://clawhub.ai/user/dazhanggui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who need courier pickup orders can use this skill to gather required shipment details, prepare the Guoguo MCP request, submit an order, and report the order ID, pickup code, account ID, or failure reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and transmits personal shipment information, including account phone numbers, sender and receiver details, full addresses, and pickup time. <br>
Mitigation: Confirm all account, sender, receiver, address, and pickup-time details with the user before sending data to the Guoguo MCP service. <br>
Risk: The skill can create real courier shipment orders through the connected MCP service. <br>
Mitigation: Require explicit user approval before submitting the order and clearly show the resulting order ID, pickup code, account ID, or failure reason. <br>
Risk: The skill may attempt persistent MCP setup when the Guoguo server is not already configured. <br>
Mitigation: Ask for approval before changing MCP configuration, review the setup behavior, and use the skill only when the publisher and Guoguo MCP service are trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce courier order identifiers, pickup codes, account IDs, and failure explanations after MCP execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
