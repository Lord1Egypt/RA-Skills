## Description: <br>
Query McDonald's China MCP server via the mcd-cn CLI for campaign calendars, coupons, and auto-claiming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanchen01](https://clawhub.ai/user/ryanchen01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check McDonald's China campaign calendars and coupon information through the mcd-cn CLI, including optional JSON output for scripts. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The MCP token can grant access to account-specific coupon actions if exposed. <br>
Mitigation: Store MCDCN_MCP_TOKEN like a password and avoid committing it in .env files or logs. <br>
Risk: The auto-bind-coupons command can claim coupons on the user's account. <br>
Mitigation: Run auto-bind-coupons only when the user explicitly intends to claim coupons. <br>
Risk: Installation depends on a third-party Homebrew tap and CLI. <br>
Mitigation: Install only after deciding to trust the ryanchen01 tap and the mcd-cn binary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanchen01/mcd-cn) <br>
- [Publisher profile](https://clawhub.ai/user/ryanchen01) <br>
- [Declared homepage](https://github.com/ryanchen01/mcd-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mcd-cn binary and MCDCN_MCP_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
