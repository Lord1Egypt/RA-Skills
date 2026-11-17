## Description:

Creates a self-contained interactive HTML snapshot of a US stock index, with market-cap-sized sector tiles colored by price moves and available sentiment, SentiSense Score, mention-volume, or options-interest readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to create an interactive snapshot for exploring US index moves by sector and, when available, market sentiment and activity overlays. The snapshot is for research and education, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refreshing a chart can replace the file at the selected destination.

Mitigation: Choose an output path that is safe to overwrite when refreshing.

Risk: An optional agent name is sent to the SentiSense provider, and the generated HTML may be too large for some inline display surfaces.

Mitigation: Avoid sending a sensitive agent name and check size warnings before displaying inline; provide the HTML as a file when needed.

Risk: The live service was not tested, and the chart is a snapshot with delayed prices and analytical readings that can have different as-of times.

Mitigation: Check the displayed as-of times and treat the chart as a dated research snapshot rather than live market data.

## Reference(s):

- [SentiSense API reference](https://sentisense.ai/skill.md)
- [SentiSense website](https://sentisense.ai)
- [ClawHub release page](https://clawhub.ai/thesentitrader/skills/market-heatmap)

## Skill Output:

**Output Type(s):** [HTML, Market data visualization]

**Output Format:** [Self-contained interactive HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A point-in-time snapshot with embedded data; the page makes no network calls and contains no API key. Price and analytical readings have separate as-of times.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
