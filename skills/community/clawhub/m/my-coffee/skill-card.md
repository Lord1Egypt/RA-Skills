## Description: <br>
My Coffee helps agents search Luckin Coffee stores and products, create pickup orders, present payment QR codes, check order status, and cancel orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckin](https://clawhub.ai/user/luckin) <br>

### License/Terms of Use: <br>
Creative Commons Attribution-NoDerivatives 4.0 International <br>


## Use Case: <br>
External users and agents use this skill to place and manage real Luckin Coffee pickup orders, including store selection, product matching, order preview, payment QR code presentation, status lookup, and cancellation. It is intended for pickup workflows only and does not support delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real Luckin pickup orders and produce payment QR codes. <br>
Mitigation: Use it only when the user intends to place a real pickup order, and confirm the store, items, price preview, and pickup flow before payment. <br>
Risk: The skill can reuse payment-order tokens from chat history or save tokens locally. <br>
Mitigation: Prefer a configured MCP secret or LUCKIN_MCP_TOKEN environment variable, avoid pasting tokens into chat, and decline local token saving unless reuse is intended. <br>
Risk: Approximate IP-based location lookup can expose coarse location and may select the wrong area. <br>
Mitigation: Provide a store, address, or coordinates manually when location privacy or accuracy matters, and do not rely on IP-derived distance as precise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckin/my-coffee) <br>
- [Luckin my-coffee MCP endpoint](https://gwmcp.lkcoffee.com/order/user/mcp) <br>
- [IP location lookup service](https://ipinfo.io/json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with order details, payment QR code links, concise guidance, and optional MCP HTTP command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the my-coffee MCP service or its HTTP endpoint with a Luckin MCP token and may display payment QR code URLs for pickup orders.] <br>

## Skill Version(s): <br>
0.8.2 (source: server release metadata, artifact metadata, manifest.json, and changelog released 2026-06-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
