## Description:

McDonald's China assistant for querying and claiming coupons, viewing campaign calendars, checking menu nutrition, and finding stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-yu](https://clawhub.ai/user/hi-yu)

### License/Terms of Use:


## Use Case:

External users can use this skill to ask an agent for McDonald's China coupon availability, coupon claiming, campaign timing, menu nutrition, calorie-aware meal suggestions, and store information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses MCD_TOKEN for account-related McDonald's coupon requests.

Mitigation: Keep the token out of logs, shared terminals, and public prompts, and rotate it if exposure is suspected.

Risk: The configurable MCD_MCP_URL endpoint receives authenticated requests.

Mitigation: Use only a trusted MCP endpoint, preferably the documented default unless there is a verified reason to change it.

Risk: One-click coupon claiming modifies account state.

Mitigation: Confirm with the user before invoking automatic coupon-claiming actions.

Risk: Coupon, campaign, and nutrition data may change or calls may be rate limited.

Mitigation: Query live data when answering time-sensitive questions and retry later after rate-limit errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hi-yu/skills/mcdonald-cn)
- [McDonald's China MCP service](https://mcp.mcd.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional tables, JSON-derived summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require MCD_TOKEN and an optional MCD_MCP_URL endpoint configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
