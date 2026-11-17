## Description:

Scrapingdog (scrapingdog.com). Use this skill for ANY Scrapingdog request — searching and reading data. Whenever a task involves Scrapingdog, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through the oo CLI to search Scrapingdog and retrieve web, Google Search, Google Maps, Google Scholar, and account usage data using their connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback instructs the agent to execute downloaded CLI installer code without an explicit approval step; the CLI implementation and external installer were not verified.

Mitigation: Review and approve the CLI installation separately before enabling the setup fallback.

Risk: Searches use connected OOMOL and Scrapingdog accounts and may consume credits.

Mitigation: Check the connected account and available credit before running searches, and monitor usage through the account usage action.

## Reference(s):

- [Scrapingdog API documentation](https://docs.scrapingdog.com/)
- [Scrapingdog](https://www.scrapingdog.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API results, JSON, Text]

**Output Format:** [JSON responses containing retrieved page HTML, parsed search results, place details, or account usage data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response fields depend on the selected Scrapingdog action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
