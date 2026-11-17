## Description:

Use the oo CLI to discover and run McDonald's China MCP actions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected McDonald's China account can discover available MCP tools and run supported ordering, coupon, campaign, and points actions. The skill guides users to inspect live action schemas and confirm state-changing requests.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Setup uses a remote installer that was not verified in this review, and the dependency can change other installed agent skills.

Mitigation: Review and verify the CLI installation before allowing setup; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: Connector actions may use account data or change order, address, coupon, or points state.

Mitigation: Review the action schema and exact request, then confirm order details, addresses, and points use before approving a change.

## Reference(s):

- [McDonald's China MCP documentation](https://open.mcd.cn/mcp/doc)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses summarized as natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions change account state; confirm the exact request before making changes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
