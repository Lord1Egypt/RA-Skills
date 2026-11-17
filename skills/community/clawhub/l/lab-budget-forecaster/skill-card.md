## Description:

Forecasts lab budget runway from available budget and expense inputs while keeping assumptions and output boundaries explicit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and lab administrators use this skill to estimate grant runway, review burn rates, and identify budget warnings or bridge-funding needs from supplied budget and expense inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast assumptions or CLI options may be misunderstood, including grant end date handling.

Mitigation: Verify the actual command-line options with --help and manually review forecast assumptions before relying on the result.

Risk: Budget or expense inputs may include sensitive lab financial data.

Mitigation: Provide only intended budget or expense CSV data and keep generated outputs in approved workspace locations.

Risk: The skill is scoped to local budget-runway forecasting, not general data analysis.

Mitigation: Stop or switch tools when a request falls outside the documented budget forecasting workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/lab-budget-forecaster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text report with optional local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, budget runway projections, warnings, cost-cutting scenarios, bridge-funding alerts, and validation caveats.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
