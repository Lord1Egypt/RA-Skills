## Description: <br>
Identifies statistical outliers in numeric datasets and returns method details, handling recommendations, assumptions, and limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data quality teams use this skill to screen numeric datasets for statistical outliers, document the selected detection method, and decide whether to flag, investigate, remove, or winsorize unusual values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python workflow reads the dataset path supplied with --data. <br>
Mitigation: Pass only intended dataset files and run the skill from a controlled workspace. <br>
Risk: Unpinned numpy and scipy dependencies may change behavior or inherit upstream vulnerabilities over time. <br>
Mitigation: Use a virtual environment and pin vetted dependency versions before production use. <br>
Risk: Outlier handling recommendations can be misleading if applied without domain review. <br>
Mitigation: Treat recommendations as analysis support and review detected outliers against domain context before removing or winsorizing data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/outlier-detection-handler) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured sections and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report outlier counts, indices, values, detection method details, assumptions, risks, and next checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
