## Description:

Operates Moojing Market Intelligence for market research and price monitoring through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and operators use this skill to inspect Moojing market, product, shop, and regional data, and to manage price-monitoring items and shops. Changes to monitoring data require confirmation as described by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute remote installer code that was unavailable for inspection, and startup synchronization may add persistent agent skills.

Mitigation: Review the installation before allowing setup, prefer a verified fixed release, and set OO_SKILLS_SYNC_DISABLED if startup skill synchronization is not wanted.

Risk: Actions can change or remove monitoring data in the connected Moojing account.

Mitigation: Use appropriate account permissions and retain the skill's confirmation requirements for write and destructive actions.

## Reference(s):

- [Moojing Market Intelligence](https://www.mktindex.com/)
- [Moojing API documentation](https://doc.mktindex.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-mktindex)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Structured Moojing data with concise text summaries; shell commands for requested actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data and results depend on the selected action and the connected Moojing account.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
