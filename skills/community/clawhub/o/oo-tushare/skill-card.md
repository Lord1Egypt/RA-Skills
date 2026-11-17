## Description:

Use Tushare through an OOMOL-connected account to search and read market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search Tushare and retrieve market data, including A-share quotes, stock information, trading calendars, and valuation indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested remote CLI installers and server implementation have not been independently verified; setup may execute downloaded code and affect agent configuration.

Mitigation: Review the setup before installing, use a separately reviewed CLI installation, and control automatic skill synchronization.

Risk: Connecting Tushare shares the API key and queries with OOMOL and may incur charges.

Mitigation: Review the account and service terms before connecting, limit queries to the intended use, and monitor usage and costs.

## Reference(s):

- [Tushare](https://tushare.pro)
- [Tushare API documentation](https://tushare.pro/document/1?doc_id=130)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Normalized JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Tushare action and the connected account's access.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
