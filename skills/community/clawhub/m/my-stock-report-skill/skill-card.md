## Description:

When explicitly invoked as a report or stock analysis engine, this skill runs a Python workflow for U.S. stock analysis, supports analyst-module selection, and archives conclusions and reports to DingTalk documents and tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agent users use this skill to generate U.S. stock analysis reports for selected tickers, choose analysis modules, and archive the resulting decision, summary, timestamp, and report links in DingTalk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically uploads generated report contents to a fixed DingTalk workspace and document/table destination.

Mitigation: Confirm the DingTalk destination before use, and use a local-only or confirmation-gated variant when reports may contain sensitive research or proprietary notes.

Risk: The skill runs local analysis commands using ticker, analyst-module, and language inputs.

Mitigation: Restrict ticker, analyst, and language values to known-safe, expected options before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown table with analysis status and archived report fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final output is expected to summarize six fields: ticker, analysis time, decision, summary, conclusion document link, and full report link.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
