## Description: <br>
Reviews C/C++ source files in a specified local directory for production readiness, code quality, and potential vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzy-creator](https://clawhub.ai/user/zhouzy-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local C/C++ codebases for memory safety, resource management, concurrency, performance, modernization, and production-readiness issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local directories selected by the user, which may expose secrets or unrelated proprietary code if scoped too broadly. <br>
Mitigation: Point the skill only at directories intended for review and avoid broad paths that may contain secrets or unrelated code. <br>
Risk: Generated review findings and fix examples may be incomplete, incorrect, or unsuitable for a specific production codebase. <br>
Mitigation: Have qualified maintainers review the generated report and proposed changes before sharing or applying them. <br>


## Reference(s): <br>
- [Local code reviewer interaction template](artifact/local-code-reviewer.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown review report with severity-ranked findings and code fix examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, line references, issue categories, deployment readiness guidance, and before/after code snippets.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
