## Description: <br>
系统化调试 guides agents through hypothesis-driven debugging: observe, hypothesize, isolate, verify, and fix, with binary-search isolation and minimal reproducer generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to investigate bugs, performance issues, regressions, and intermittent failures by collecting evidence before making code changes. It helps structure hypotheses, isolate likely causes, generate minimal reproducers, and document root-cause findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad bug or error reports and slow down tasks that need a narrower workflow. <br>
Mitigation: Use a more specialized skill explicitly when the task calls for a different debugging or remediation workflow. <br>
Risk: Premature or weakly supported hypotheses can lead to misleading fixes. <br>
Mitigation: Require collected evidence, minimal reproduction, and regression validation before applying code changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-systematic-debug) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with structured debugging notes and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hypothesis lists, evidence logs, minimal reproducer guidance, binary-search isolation steps, root-cause reports, and proposed regression tests.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
