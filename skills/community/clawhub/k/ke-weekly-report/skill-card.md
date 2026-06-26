## Description: <br>
Generates structured workplace weekly, monthly, review, and project reports from user-provided work notes, with the included implementation producing local Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoheizp](https://clawhub.ai/user/xiaoheizp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, freelancers, and students can use this skill to turn work-log notes into structured status reports for weekly updates, monthly summaries, review materials, and project closeout reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Work-log inputs may contain confidential project, customer, or personnel information. <br>
Mitigation: Review or redact sensitive details before pasting work logs into an agent workflow. <br>
Risk: The documentation advertises Word/PPT, batch, file-input, style, and output-path features that the included code does not implement in this version. <br>
Mitigation: Use this release as a basic local Markdown report formatter and verify generated reports before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoheizp/ke-weekly-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report text with optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included code reads a command-line text argument and prints a Markdown weekly report; Pandoc is documented as an optional dependency for conversions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
