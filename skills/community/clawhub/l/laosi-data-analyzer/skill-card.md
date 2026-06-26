## Description: <br>
Loads CSV or JSON datasets, computes descriptive statistics, detects outliers, estimates trends, calculates correlations, and can save a local JSON analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to inspect CSV or JSON datasets, summarize numeric columns, identify outliers, compare correlations, and generate a local analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive CSV or JSON contents may be exposed through local analysis or saved reports. <br>
Mitigation: Use only datasets appropriate for local analysis, and avoid highly sensitive data unless local report storage is acceptable. <br>
Risk: A generated report could overwrite an existing local file if the same output path is reused. <br>
Mitigation: Specify a clear, non-conflicting output filename before saving reports. <br>


## Reference(s): <br>
- [Data Analyzer Pro on ClawHub](https://clawhub.ai/534422530/laosi-data-analyzer) <br>
- [Publisher profile 534422530](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, JSON, guidance] <br>
**Output Format:** [Markdown guidance with Python code and optional JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read user-selected CSV or JSON files and write a local JSON report when an output path is provided.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
