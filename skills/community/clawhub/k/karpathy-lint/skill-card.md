## Description: <br>
Performs quality checks on Karpathy LLM knowledge points, including duplicate detection, completeness checks, tag validation, and health-report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base maintainers use this skill to inspect local Karpathy LLM knowledge-point Markdown files for duplicates, incomplete entries, weak tags, and other health issues. It produces a local report with statistics and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local knowledge-point Markdown files and writes a local health report. <br>
Mitigation: Confirm the intended knowledge directory before running so reports and any explicitly saved revisions go where expected. <br>
Risk: Duplicate repair behavior can merge or remove knowledge-point entries when used programmatically. <br>
Mitigation: Review proposed duplicate findings and keep a backup of knowledge-point files before applying any repair flow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sora-mury/karpathy-lint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown report and text findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local knowledge-point Markdown files and can write a local lint report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
