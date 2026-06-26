## Description: <br>
Compares two JSON files or objects deeply, supports unordered list comparison and ignored fields, and produces a structured Excel difference report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanw2039](https://clawhub.ai/user/hanw2039) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to validate API responses, compare configuration files, and check data migration results by finding field-level JSON differences and exporting them to Excel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input JSON values may include personal data, credentials, tokens, or business data that are copied into the generated Excel report. <br>
Mitigation: Treat generated reports as sensitive files, review them before sharing, and avoid comparing secret-bearing JSON unless the report is stored and handled securely. <br>
Risk: The skill reads local JSON files and writes a local Excel file, so incorrect paths can expose or overwrite local data. <br>
Mitigation: Run it from a controlled working directory, pass explicit input and output paths, and review the output location before execution. <br>
Risk: Large JSON files can take a long time to process. <br>
Mitigation: Follow the artifact guidance to keep files at manageable sizes, around 100MB or less, or split very large comparisons into smaller units. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanw2039/json-deep-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands; generated runtime output is a structured Excel report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts two JSON inputs, optional ignored fields, optional strict array ordering, and an optional Excel output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
