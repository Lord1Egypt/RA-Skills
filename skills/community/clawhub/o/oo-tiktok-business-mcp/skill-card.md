## Description:

Runs TikTok for Business MCP actions through an OOMOL-connected account, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advertising operators use this skill to read and manage TikTok for Business data through an OOMOL-connected account. Confirm write or destructive actions before changing advertising assets, budgets, delivery, or access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup executes remote installer code that has not been verified.

Mitigation: Use a vetted CLI release and inspect downloaded installers before running them.

Risk: Startup skill synchronization can make persistent changes across agent hosts.

Mitigation: Disable startup skill synchronization if cross-host skill updates are not wanted.

Risk: TikTok advertising actions can affect budgets, delivery, access, or assets.

Mitigation: Limit TikTok authorization and retain the required user approvals for advertising changes.

## Reference(s):

- [TikTok for Business](https://business.tiktok.com)
- [TikTok Business API documentation](https://business-api.tiktok.com/portal/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-tiktok-business-mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JSON action results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change TikTok advertising data; changes require the documented user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
