## Description: <br>
MergeGuard reviews AI-generated code before merge and returns a strict merge decision covering correctness, scope, security/privacy, dependency/config risk, tests, validation evidence, and required fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use MergeGuard to evaluate PRs, diffs, patches, generated code, local changes, or agent-written output before merge. It helps decide whether to merge, fix first, reject, or block pending more evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incomplete review context can lead to an incorrect merge recommendation. <br>
Mitigation: Review only visible evidence and use FIX FIRST or BLOCKED when important code, CI, test output, or acceptance criteria are missing. <br>
Risk: Code, diffs, PR context, or test output shared for review may contain secrets or sensitive data. <br>
Mitigation: Provide the least necessary context, redact credentials and private data before review, and treat any detected exposure as a security finding. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown review with structured decision, risk, confidence, findings, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one of MERGE, FIX FIRST, REJECT, or BLOCKED as the decision.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
