## Description:

Provides real-time market price lookup for 25,000+ crypto, equity, forex, ETF, commodity, and global index assets through the Juglans Finance API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juglans-ai](https://clawhub.ai/user/juglans-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in Claude Code to answer stock, crypto, forex, ETF, commodity, and index price questions with live API data instead of model guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer uses unverified mutable remote downloads.

Mitigation: Prefer the ClawHub package or a locally inspected SKILL.md; do not use the curl-to-bash flow unless the publisher pins it to a reviewed immutable release and provides integrity verification.

Risk: The installer references a different repository path than the README installation examples.

Mitigation: Review and correct the installer repository target before trusting the remote installation flow.

Risk: Market data can be unavailable, stale outside market hours, or missing for an unsupported symbol.

Mitigation: Report missing API data honestly, disclose when prices are last-close values, and avoid fabricating prices or market attributes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juglans-ai/skills/market-price)
- [Juglans Finance](https://finance.juglans.ai)
- [Juglans Finance Ticker API](https://finance.juglans.ai/api/v1/ticker?id={IDENTIFIER})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown responses with inline shell commands and parsed API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Bash/curl calls to the Juglans Finance API; no API key is described.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
