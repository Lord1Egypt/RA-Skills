## Description:

Provides multi-source real-time and historical Chinese stock market data with rate limiting, failover, and technical indicator calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul1989889](https://clawhub.ai/user/paul1989889)

### License/Terms of Use:

MIT License

## Use Case:

Developers and analysts use this skill to retrieve Chinese stock quotes and K-line data from Tencent, AKShare, and Baostock, then calculate common technical indicators for market analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may resolve to different package versions over time.

Mitigation: Install in a virtual environment and pin or lock dependencies before production use.

Risk: The skill contacts public market-data providers during normal use.

Mitigation: Run it only where external network access to those providers is approved and keep rate limiting enabled.

Risk: Generated buy or sell indicator labels may be mistaken for investment advice.

Mitigation: Treat indicator labels as analytical signals and review them with appropriate financial judgment before acting.

Risk: The example script can create CSV files in the working directory.

Mitigation: Run examples from a controlled workspace and review generated files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul1989889/skills/market-data-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate CSV files when running the example script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
