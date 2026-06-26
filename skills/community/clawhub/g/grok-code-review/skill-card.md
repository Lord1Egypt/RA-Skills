## Description: <br>
Perform expert, security-first code reviews for code, diffs, pull requests, and implementations, with attention to bugs, security issues, quality, performance, and maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit source code, diffs, and pull requests for security, correctness, quality, performance, and maintainability risks before approval or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review output may include incorrect findings or fixed-code examples that could introduce defects if applied without validation. <br>
Mitigation: Treat recommendations as advisory, review proposed changes, and run the relevant tests before merging or deploying. <br>
Risk: Powerful maintenance workflows may use broad tool access in environments where nested review defaults allow full access. <br>
Mitigation: Install only in intended ClawHub/Convex maintenance environments and use --no-yolo when nested review should not bypass sandbox prompts. <br>
Risk: Untrusted code or diffs may contain instructions that try to influence the reviewing agent. <br>
Mitigation: Use the artifact's static-analysis posture: inspect code as evidence, do not execute untrusted code, and require explicit confirmation before modifying systems or data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/grok-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured Markdown review report with severity sections, fixed-code examples, and an approval recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static analysis and advisory output only; the skill instructs agents not to execute untrusted code and to require confirmation before actions that modify systems or data.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
