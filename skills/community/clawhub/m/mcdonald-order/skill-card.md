## Description:

McDonald's China assistant (麦当劳助手) for coupon management, delivery ordering, and nutrition planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lililisir](https://clawhub.ai/user/lililisir)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to interact with McDonald's China services for coupon discovery and claiming, delivery ordering, menu and price lookup, nutrition planning, promotion checks, and order tracking.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: A configurable endpoint can redirect the user's McDonald's bearer token.

Mitigation: Remove or tightly control any `MCD_MCP_URL` override and prefer network egress limited to `https://mcp.mcd.cn`.

Risk: The skill receives a McDonald's account token and can run shell commands.

Mitigation: Install only from a trusted source, use a revocable token if available, and review the skill before use.

Risk: Coupon, address, and order actions may change account state or create purchase flows.

Mitigation: Manually confirm coupon, address, price, and order actions before they run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lililisir/skills/mcdonald-order)
- [McDonald's China MCP service](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, numbered lists, plain-language guidance, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coupon lists, menu and price summaries, nutrition tables, order status summaries, and confirmation prompts before account-changing actions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
