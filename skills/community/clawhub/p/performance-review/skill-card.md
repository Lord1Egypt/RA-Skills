## Description: <br>
Generates performance review drafting templates for self-assessments, manager feedback, KPI summaries, promotion narratives, SMART goals, and 360 feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and HR-adjacent reviewers use this skill to draft structured performance review materials from role, achievement, KPI, goal, or feedback prompts. It is best suited for local drafting workflows where the user reviews and edits the generated text before sharing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Performance review prompts may include confidential HR or employee details. <br>
Mitigation: Avoid entering sensitive personal or HR information unless local shell history, terminal output, and any saved files are acceptable for that data. <br>
Risk: The bundled generic helper script can log command arguments to local history files if invoked. <br>
Mitigation: Use the documented review script for drafting workflows and inspect local data directories before entering sensitive arguments. <br>
Risk: Generated review text may overstate achievements or produce wording that needs manager or employee validation. <br>
Mitigation: Review generated drafts against real evidence, metrics, and company performance-review policy before sharing or submitting them. <br>


## Reference(s): <br>
- [Performance Review skill page](https://clawhub.ai/ckchzh/performance-review) <br>
- [绩效评估使用技巧与最佳实践](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown-style review templates produced by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local command output; no external dependencies are required by the primary review script.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
