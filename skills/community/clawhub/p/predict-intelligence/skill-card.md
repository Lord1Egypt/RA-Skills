## Description: <br>
Predict intelligence skill for AI agents that generates professional PDF reports with probability-ranked predictions, D3 visualizations, and Polymarket consensus signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ken-Chy129](https://clawhub.ai/user/Ken-Chy129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to research prediction questions and produce concise intelligence briefs with calibrated outcomes, source-backed drivers, watch lists, visualizations, and optional Polymarket comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may browse the web, query Polymarket, execute Python and Playwright, and write local HTML/PDF files. <br>
Mitigation: Run it in a virtual environment with expected file-write locations and review generated reports before using them for financial or operational decisions. <br>
Risk: Generated reports may load assets from third-party CDNs. <br>
Mitigation: Use only in environments where those external loads are acceptable, or review the HTML template before rendering. <br>
Risk: Prediction outputs can be incorrect, incomplete, or stale. <br>
Mitigation: Verify source URLs, probabilities, and market data before relying on the report. <br>


## Reference(s): <br>
- [Predict Intelligence Skill Page](https://clawhub.ai/Ken-Chy129/predict-intelligence) <br>
- [Data Sources & Methodology Reference](artifact/reference.md) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket Event Pages](https://polymarket.com/event/{slug}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [HTML report converted to PDF, with Markdown guidance and inline shell commands during agent execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HTML/PDF report files and may query web sources and Polymarket for current prediction data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
