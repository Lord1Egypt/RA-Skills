## Description:

Search and retrieve cryptocurrency market data from Coinranking through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use the skill to search Coinranking and retrieve coin details, price history, supported reference currencies, and global market statistics. The agent can use the returned data to answer cryptocurrency research questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup instructions can execute downloaded installer code that this review did not verify.

Mitigation: Install a pinned, integrity-verified oo CLI yourself and prevent automatic execution of fallback installers.

Risk: The oo CLI's bundled-skill synchronization runs at startup and was identified for review.

Mitigation: Review its synchronization behavior; set OO_SKILLS_SYNC_DISABLED to disable startup synchronization if needed.

## Reference(s):

- [Coinranking homepage](https://coinranking.com)
- [Coinranking API documentation](https://coinranking.com/api/documentation)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables and synchronization](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, JSON data]

**Output Format:** [Coinranking response data as JSON, with text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search and market data retrieval]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
