## Description:

Measure US equity market breadth using advance/decline lines, percentage of stocks above moving averages, and new highs/lows via the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess US equity market breadth, detect breadth divergences, and summarize market health from Finskills API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends market-analysis requests to Finskills using the configured API key.

Mitigation: Use an appropriate Finskills API key, protect it as a secret, and avoid sending data you do not want processed by Finskills.

Risk: Market health reports may include positioning suggestions based on third-party market data.

Mitigation: Treat outputs as informational and review investment decisions before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/market-breadth-analyzer)
- [Project homepage](https://github.com/finskills/market-breadth-analyzer)
- [Finskills](https://finskills.net)
- [Finskills registration](https://finskills.net/register)
- [Market breadth endpoint](https://finskills.net/v1/free/market/breadth)
- [Market summary endpoint](https://finskills.net/v1/market/summary)
- [Short volume endpoint](https://finskills.net/v1/free/market/short-volume-top)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown market breadth report with calculated indicators and positioning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Finskills market data and requires FINSKILLS_API_KEY.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
