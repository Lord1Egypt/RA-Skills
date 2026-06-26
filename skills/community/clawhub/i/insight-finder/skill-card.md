## Description: <br>
Insight Finder analyzes CSV, JSON, Excel, and pasted tabular data to produce structured statistical insight reports with confidence ratings, limitations, and recommended actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softboypatrick](https://clawhub.ai/user/softboypatrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to explore datasets, assess data quality, discover statistical relationships, identify anomalies, and turn findings into decision-oriented reports. It is most useful when an agent is given tabular data or a data file path and asked to find patterns or produce an analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process confidential, regulated, or production data when users paste datasets or provide file paths. <br>
Mitigation: Use only data that is appropriate for the agent environment, redact sensitive fields before analysis, and confirm organizational approval before processing regulated data. <br>
Risk: Statistical findings may be hypotheses rather than proven causes. <br>
Mitigation: Review the generated report, check stated limitations, and validate high-impact recommendations with additional analysis or controlled experiments before acting on them. <br>
Risk: The skill may activate on broad data-analysis requests or pasted tabular content. <br>
Mitigation: Confirm the intended dataset and scope before running the analysis when the user request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/softboypatrick/insight-finder) <br>
- [Publisher profile](https://clawhub.ai/user/softboypatrick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with statistics, findings, confidence ratings, limitations, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data quality scores, statistical test results, effect sizes, anomaly notes, chart descriptions, and explicit limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
