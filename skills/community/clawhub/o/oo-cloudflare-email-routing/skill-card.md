## Description:

Cloudflare Email Routing (cloudflare.com). Use this skill for ANY Cloudflare Email Routing request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare Email Routing, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect destination addresses and routing rules, or to create, update, and delete Cloudflare Email Routing rules through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute downloaded code without separate approval.

Mitigation: Review the setup and prefer a reviewed, version-pinned installation before use.

Risk: Setup may introduce persistent changes to other agent apps.

Mitigation: Configure the startup skill-sync control before use and review persistent changes.

Risk: Creating, updating, or deleting routing rules can affect email delivery.

Mitigation: Connect only the Cloudflare permissions needed and retain approval for routing changes.

## Reference(s):

- [Cloudflare Email Routing API documentation](https://developers.cloudflare.com/api/resources/email_routing/)
- [Cloudflare Email Routing](https://www.cloudflare.com/developer-platform/products/email-routing/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON connector results with concise text summaries and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses action-specific input schemas; changes to routing rules require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
