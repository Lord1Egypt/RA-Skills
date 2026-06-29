## Description: <br>
Systematic quality review for code, skills, configurations, and documents using GLIC or UGLIC dimensions with cited findings and severity tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, and technical reviewers use Glic Check to run structured multi-dimension reviews of code, agent skills, configuration, and documentation before accepting changes or releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad quality-review requests may activate the skill and cause it to read the target files selected for audit. <br>
Mitigation: Confirm the intended scope before running when the target is ambiguous, and limit the review to files the user wants audited. <br>
Risk: The review report may contain incorrect or misleading findings or proposed fixes. <br>
Mitigation: Review cited locations and severity tags before approving any changes. <br>
Risk: The optional anti-pattern pre-scan only surfaces candidates and can produce false positives. <br>
Mitigation: Treat pre-scan output as triage input and require full checklist review with precise citations before reporting a finding. <br>


## Reference(s): <br>
- [Glic Check ClawHub listing](https://clawhub.ai/songhonglei/glic-check) <br>
- [dimensions.md](artifact/references/dimensions.md) <br>
- [output-format.md](artifact/references/output-format.md) <br>
- [examples.md](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with file:line citations, severity tags, a summary table, and a fix prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are grouped by GLIC or UGLIC dimensions and tagged ERR, WARN, or INFO.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
