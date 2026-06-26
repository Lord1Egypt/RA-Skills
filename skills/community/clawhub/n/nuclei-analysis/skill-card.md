## Description: <br>
Intelligently analyzes Nuclei scan results, prioritizes real bugs, reduces noise, and enriches findings with context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyetnighy](https://clawhub.ai/user/nyetnighy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External security testers, bug bounty hunters, and security engineers use this skill to turn completed Nuclei scan output into prioritized Markdown triage reports with severity summaries, high-impact detail, attack scenarios, and reproduction steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filtered findings, severity changes, attack scenarios, or reproduction steps may be incomplete or misleading if accepted without reviewing the original Nuclei output. <br>
Mitigation: Review the original Nuclei findings and validate high-impact security decisions before acting on the generated report. <br>
Risk: The helper reads local scan files and writes Markdown reports, which may capture sensitive target information. <br>
Mitigation: Run it only on intended scan outputs and handle generated reports according to the user's data handling policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyetnighy/nuclei-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with summary tables, prioritized findings, attack scenarios, and reproduction steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under reports/nuclei-analysis/ by default; supports minimum-severity filtering and explicit output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
