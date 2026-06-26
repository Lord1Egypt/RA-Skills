## Description: <br>
McDonald's China assistant for coupon management, delivery ordering, menu and price queries, nutrition planning, promotions, and order tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lililiSir](https://clawhub.ai/user/lililiSir) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to interact with McDonald's China services for coupons, delivery ordering, menu prices, nutrition information, promotions, and order tracking. It is intended for supervised use because account actions and ordering require user confirmation. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a McDonald's account token together with shell-based curl access. <br>
Mitigation: Install only from a trusted publisher, review the artifact before use, and keep MCD_TOKEN private. <br>
Risk: The optional MCD_MCP_URL endpoint can redirect sensitive authenticated requests. <br>
Mitigation: Leave MCD_MCP_URL unset or set it only to https://mcp.mcd.cn. <br>
Risk: Coupon claiming, address creation, coupon use, and order creation can affect the user's account or purchases. <br>
Mitigation: Run the skill under user supervision and require explicit confirmation before any account-changing or order-related action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lililiSir/mcdonald-order) <br>
- [McDonald's China MCP service](https://mcp.mcd.cn) <br>
- [README](artifact/README.md) <br>
- [Security considerations](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with Chinese user-facing text, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call McDonald's China MCP tools through curl using MCD_TOKEN and an optional MCD_MCP_URL endpoint.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
