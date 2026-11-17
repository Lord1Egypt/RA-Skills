## Description:

PairPulse helps agents run local market basket analysis on Excel order data and produce Apriori association rules, structured JSON results, charts, and business strategy suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucetam-sino](https://clawhub.ai/user/brucetam-sino)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, data analysts, ecommerce operators, and consultants use PairPulse to analyze order spreadsheets, find products commonly bought together, and generate recommendations for bundles, page recommendations, merchandising, promotions, and add-on sales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to install or upgrade an unpinned PyPI package before processing local order spreadsheets.

Mitigation: Review the PairPulse package and source before use, install it in a virtual environment or container, and pin a reviewed version instead of auto-upgrading.

Risk: The tool reads customer order spreadsheets and may access files or directories the agent can reach.

Mitigation: Run PairPulse only on spreadsheets and directories intended for analysis, and avoid exposing unrelated sensitive files to the agent session.

## Reference(s):

- [ClawHub PairPulse Skill Page](https://clawhub.ai/brucetam-sino/skills/pairpulse)
- [PairPulse GitHub Project Link Declared in Artifact](https://github.com/brucetam-sino/PairPulse)

## Skill Output:

**Output Type(s):** [shell commands, json, markdown, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can also produce Excel reports and PNG charts according to the artifact.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
