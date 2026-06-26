## Description: <br>
Creates formula-driven Excel dashboards and executive summaries from CSV or tabular data, delivering a single .xlsx workbook with data and Dashboard sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to turn CSV or tabular datasets into polished Excel KPI dashboards with formula-driven metrics, charts, sparklines, conditional formatting, and validation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to download and run an unpinned officecli installer or upgrade script before use. <br>
Mitigation: Review before installing; prefer installing a verified, pinned officecli version yourself and disabling or ignoring the automatic install or upgrade block. <br>
Risk: Dashboard outputs can contain misleading formulas, blank charts, or layout issues if the workbook is not validated. <br>
Mitigation: Follow the included QA checklist, run officecli validation, and verify formulas, chart data ranges, and Dashboard rendering before delivery. <br>


## Reference(s): <br>
- [creating.md](creating.md) <br>
- [ClawHub skill page](https://clawhub.ai/iceyliu/officecli-data-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [XLSX workbook with Markdown/text guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one .xlsx file with imported data, a Dashboard sheet, formula-driven KPIs, charts, sparklines, conditional formatting, and validation steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
