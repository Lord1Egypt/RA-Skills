## Description: <br>
Checks undergraduate and graduate thesis formatting against school-specific or default rules, proposes and applies automated fixes where supported, and generates before-and-after comparison reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sashavegal](https://clawhub.ai/user/sashavegal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, academic staff, and writing-support developers use this skill to inspect thesis .docx files, compare them with university formatting requirements, apply supported formatting repairs, and produce review reports. When no school rules are supplied, it uses a built-in default rule set based on common Chinese thesis conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write repaired document files and reports that may include thesis excerpts or document metadata. <br>
Mitigation: Use copies of important thesis files, choose a separate output path, and keep generated reports private. <br>
Risk: Automated formatting changes may not satisfy every school rule or submission requirement. <br>
Mitigation: Review all formatting changes and manually confirm unsupported items before submitting academic work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sashavegal/paper-check) <br>
- [Format rules template](references/format_rules_template.md) <br>
- [Common thesis formatting issues](references/common_issues.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated .docx reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create repaired thesis documents and comparison reports that include thesis excerpts and document metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
