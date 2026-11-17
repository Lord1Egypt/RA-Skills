## Description:

Search and read FinChina company, financial, enterprise-risk, and metadata information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can query FinChina for company profiles, financial metrics, enterprise-risk information, and indicator metadata through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance relies on remote CLI installers and connector behavior that have not been verified.

Mitigation: Review and install a verified CLI release yourself before enabling the skill.

Risk: Startup skill synchronization can make persistent changes to installed agent skills, and those changes are insufficiently disclosed.

Mitigation: Consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the CLI reference.

Risk: FinChina queries use the connected account and may consume credits.

Mitigation: Check the requested query and account credit implications before running it.

## Reference(s):

- [FinChina](https://mcp.finchina.com)
- [FinChina API documentation](https://mcp.finchina.com/guide/mcp/tools/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [FinChina ClawHub release](https://clawhub.ai/oomol/skills/oo-finchina)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured FinChina query results, commonly JSON, with text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields depend on the selected FinChina action; account queries may consume credits.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
