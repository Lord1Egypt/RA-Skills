## Description:

Open Exchange Rates (openexchangerates.org). Use this skill for ANY Open Exchange Rates request — searching and reading data. Whenever a task involves Open Exchange Rates, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can retrieve supported currencies, current or historical exchange rates, time series, and currency conversions through an OOMOL-connected Open Exchange Rates account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup can execute downloaded CLI installation software, and the remote installer and CLI have not been audited.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release. Disable startup synchronization with OO_SKILLS_SYNC_DISABLED if you do not want the CLI managing skills in other agent applications.

Risk: Requests use the OOMOL-connected account and may consume credits.

Mitigation: Check the connected account's available credits and usage before running requests.

## Reference(s):

- [Open Exchange Rates API documentation](https://docs.openexchangerates.org/)
- [Open Exchange Rates](https://openexchangerates.org)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, API data, Shell commands]

**Output Format:** [Natural-language responses with exchange-rate data; CLI requests use JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected currency action and the connected account's access.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
