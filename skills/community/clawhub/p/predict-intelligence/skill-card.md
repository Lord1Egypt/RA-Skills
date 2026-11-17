## Description:

Predict Intelligence generates professional PDF reports with probability-ranked predictions, D3 visualizations, and Polymarket consensus signals for geopolitics, finance, technology, elections, corporate events, and other prediction questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken-chy129](https://clawhub.ai/user/ken-chy129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate source-backed prediction briefs that combine current research, probability-ranked outcomes, visualizations, and Polymarket consensus comparisons. It is intended for agents that can search the web, fetch URLs, run shell commands, and write report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF rendering executes mutable third-party JavaScript and browser tooling.

Mitigation: Run the skill in an isolated environment, pin or vendor JavaScript assets and browser/Python dependencies, and review generated HTML before PDF conversion.

Risk: The skill makes web requests, contacts Polymarket, and writes local HTML/PDF report files.

Mitigation: Use a scoped working directory, review source URLs and generated files, and restrict network access when live market or news data is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken-chy129/skills/predict-intelligence)
- [Data Sources & Methodology Reference](artifact/reference.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with HTML and PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained HTML reports, converts them to PDF with Playwright Chromium, and may include D3 visualizations and Polymarket market data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
