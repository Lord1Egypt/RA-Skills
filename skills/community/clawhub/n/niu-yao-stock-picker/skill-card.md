## Description:

NiuYao Stock Picker ranks short-term A-share candidates from recent limit-up pools using a six-factor scoring model covering theme strength, stock behavior, opening gain, turnover, market sentiment, and consecutive limit-up height.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinyan623](https://clawhub.ai/user/martinyan623)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to generate informational short-term A-share ranking reports and compare candidates from recent limit-up pools. Developers can run the included script to produce dated Markdown reports for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may generate unattended financial reports or notifications.

Mitigation: Confirm any scheduled run, push destination, and disable controls before installation.

Risk: Generated stock rankings may be mistaken for investment advice.

Mitigation: Treat rankings as informational only and validate decisions against official market data and independent review.

Risk: Runtime dependencies and live market-data access can affect reliability and execution scope.

Mitigation: Install dependencies in an isolated environment with pinned versions and review the script before use.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/martinyan623/skills/niu-yao-stock-picker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, terminal status text, and saved report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports/niu_yao_v1_YYYYMMDD.md when the scoring script runs successfully.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
