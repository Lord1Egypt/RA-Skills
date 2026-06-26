## Description: <br>
A Maldives island-planning assistant that collects trip preferences, searches travel guidance and product listings, and produces a structured island recommendation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miracleaaa](https://clawhub.ai/user/miracleaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to compare Maldives resort islands against trip type, preferred activities, transport preferences, and budget. It guides the user through requirements collection and produces a decision-ready Markdown report with ranked recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run an external npm CLI for FlyAI product lookup and send travel preferences to search or product services. <br>
Mitigation: Use the product lookup only in workspaces where external service calls are acceptable, and skip the lookup for sensitive trip details. <br>
Risk: The skill saves a local report file and can export that report to PDF. <br>
Mitigation: Check the output filename and location before export, and avoid writing reports into directories containing important files with similar names. <br>
Risk: Travel prices, availability, reviews, and resort policies can change after a report is generated. <br>
Mitigation: Treat generated recommendations as planning guidance and verify prices, booking terms, and travel requirements with current booking sources before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miracleaaa/maldives-island-picker) <br>
- [Demand collection reference](artifact/references/intent-collection.md) <br>
- [Island report template](artifact/references/report-template.md) <br>
- [PDF export script documentation](artifact/scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, product links, image embeds, and optional PDF export command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill normally saves a local Markdown report and can use a helper script to convert that report to PDF when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
