## Description: <br>
Pre-landing PR review that analyzes diffs against the base branch for SQL safety, LLM trust boundaries, conditional side effects, scope drift, missing requirements, and other structural issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loocor](https://clawhub.ai/user/loocor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before landing a pull request to review branch diffs, detect structural or safety issues, identify scope drift or missing requirements, and apply clear fixes when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly edit code while reviewing a pull request. <br>
Mitigation: Use it on a clean branch and inspect the resulting git diff before committing or pushing. <br>
Risk: The skill relies on local checklist files and optional external review flows. <br>
Mitigation: Verify referenced checklist files are present and trusted, and decline optional Codex/browser review unless sharing the relevant context is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loocor/gstack-review) <br>
- [Publisher profile: loocor](https://clawhub.ai/user/loocor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with inline shell commands and optional code edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify the working tree for auto-fixable findings and may ask batched follow-up questions for judgment-based fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
