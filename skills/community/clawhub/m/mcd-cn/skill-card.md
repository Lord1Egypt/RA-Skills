## Description:

Query McDonald's China MCP server via the mcd-cn CLI for campaign calendars, coupons, and auto-claiming. Use for human-friendly coupon lookup or JSON output for scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanchen01](https://clawhub.ai/user/ryanchen01)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query McDonald's China campaign calendars and coupons through the mcd-cn CLI, including human-readable lookups and JSON output for scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install an unpinned third-party CLI and provide an account token.

Mitigation: Review the upstream mcd-cn project and Homebrew tap before installation, and use a minimally scoped token if one is available.

Risk: The auto-bind-coupons command can change account state rather than only reading coupon data.

Mitigation: Treat auto-bind-coupons as an account-changing action and confirm intent before running it.

Risk: A token stored in a committed .env file could expose account access.

Mitigation: Set MCDCN_MCP_TOKEN in the runtime environment and avoid committing .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanchen01/skills/mcd-cn)
- [Project homepage](https://github.com/ryanchen01/mcd-cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses may be human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mcd-cn CLI and MCDCN_MCP_TOKEN; rate limit is 600 requests per minute per token.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
