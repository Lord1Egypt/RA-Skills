## Description: <br>
Iris reads a Gmail inbox, scores recent emails by urgency and sender importance, drafts replies for the top five, and produces a daily action list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use Iris to triage Gmail, identify messages needing attention, prepare draft responses, and save a local daily inbox report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive Gmail app password to read inbox data. <br>
Mitigation: Use a revocable Gmail app password, store it privately, and revoke it from Google Account settings when the skill is no longer needed. <br>
Risk: The skill saves email-derived details to a local Markdown report by default. <br>
Mitigation: Run it in a private directory, review the generated report, and delete reports that should not be retained. <br>


## Reference(s): <br>
- [Iris ClawHub skill page](https://clawhub.ai/occupythemilkyway/iris) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Console output and a local Markdown inbox report with draft reply text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail address and Gmail app password environment variables; writes an inbox_report_<date>.md file locally.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
