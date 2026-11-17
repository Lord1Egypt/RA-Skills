## Description:

Tongdaxin (vip.tdx.com.cn). Use this skill for ANY Tongdaxin request — reading, creating, updating, and deleting data. Whenever a task involves Tongdaxin, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to query Tongdaxin market, company, financial, and research information, and to carry out supported account actions through the connected service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses a remote installer that has not been verified.

Mitigation: Review the setup before installing and prefer a verified oo CLI release installed under your control.

Risk: Managed skill synchronization may make broad changes to agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if managed synchronization is unwanted.

Risk: The connector exposes a destructive action that may remove or overwrite data.

Mitigation: Connect only the intended account and retain approval for destructive actions; confirm the target and effect before running them.

## Reference(s):

- [Tongdaxin API documentation](https://help.tdx.com.cn/tdxclaw/docs/markdown/tdxclaw-api-key-data.html)
- [Tongdaxin product page](https://vip.tdx.com.cn/site/app/pc-mall/main.html#/page_product_mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [Structured connector results summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and may include current or historical financial data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
