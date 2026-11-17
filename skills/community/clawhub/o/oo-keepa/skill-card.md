## Description:

Use this skill to search Keepa and retrieve Amazon product, seller, category, deal, and historical marketplace data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find Amazon products and sellers, inspect category and deal data, and retrieve current or historical marketplace metrics from Keepa. It requires an installed, authenticated oo CLI with Keepa connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and may make broader changes to agent skills through automatic synchronization.

Mitigation: Review and verify the oo CLI installer before setup; disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED if only Keepa access is needed.

Risk: Connector requests are brokered by OOMOL and may consume account credit.

Mitigation: Check the relevant Keepa token costs and account credit before running costly requests.

## Reference(s):

- [Keepa](https://keepa.com/)
- [Keepa API Documentation](https://keepa.com/api-docs/request-basics.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON connector responses, textual summaries, and inline Bash instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some full-list requests consume Keepa tokens, and seller storefront results may be incomplete.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
