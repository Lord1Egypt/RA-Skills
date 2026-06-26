## Description: <br>
AI-native agentic commerce: 10 MCP tools to discover businesses, browse product catalogs with variants, and complete purchases with Stripe payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theoddbrick](https://clawhub.ai/user/theoddbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers connect an MCP-capable agent to LobsterSearch so it can search for businesses, inspect catalogs, check availability, create and confirm orders, generate Stripe payment links, track status, and cancel orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create orders, generate payment links, cancel orders, initiate refunds, and handle customer data through an unauthenticated hosted connector. <br>
Mitigation: Keep tool-call approval enabled and manually confirm merchant, items, totals, customer details, payment-link generation, and cancellation or refund actions before execution. <br>
Risk: Order IDs and customer details may expose private transaction information. <br>
Mitigation: Treat order IDs and customer information as private, avoid sharing them outside the intended session, and review outputs before storing or forwarding them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/theoddbrick/lobstersearch-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/theoddbrick) <br>
- [LobsterSearch homepage](https://lobstersearch.ai) <br>
- [Hosted MCP endpoint](https://mcp.lobstersearch.ai/mcp) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/examples/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON tool responses and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include next_actions, retry_guidance, order identifiers, payment state, stock availability, and Stripe Checkout payment links.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact files describe LobsterSearch server version 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
