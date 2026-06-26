## Description: <br>
Provides OpenClaw observability tools that report recent errors and estimate API usage costs over the last 24 hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erain](https://clawhub.ai/user/erain) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw bot owners, operators, and developers use this skill to view recent failures and approximate API usage costs without opening a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent error reports can expose local OpenClaw operational telemetry such as paths, stack traces, session titles, identifiers, usage amounts, and status details. <br>
Mitigation: Install only where callers are trusted to view local telemetry, and review output before forwarding it. <br>
Risk: Cost reports are estimates based on recent session data and a hardcoded pricing table, so totals can be incomplete or stale. <br>
Mitigation: Treat cost output as an operational estimate and verify pricing-sensitive decisions against provider billing records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erain/openclaw-skill-observability) <br>
- [Skill README](artifact/README.md) <br>
- [MVP product requirements](artifact/docs/PRD_MVP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text] <br>
**Output Format:** [Markdown reports and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost reports are estimates over recent sessions; error reports may include session IDs, statuses, titles, and filtered local log lines.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; package.json declares 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
