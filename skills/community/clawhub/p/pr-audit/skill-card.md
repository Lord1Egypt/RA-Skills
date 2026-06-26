## Description: <br>
Use when the user wants a local review of a GitHub pull request based on its diff, risks, quality, performance, tests, and security implications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review GitHub pull request diffs for correctness, security-sensitive changes, performance concerns, test coverage, and actionable follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pull request diffs may contain sensitive code or accidental secrets. <br>
Mitigation: Avoid sharing secrets in review prompts and use least-privileged GitHub access when fetching private pull requests. <br>
Risk: Review findings may be incomplete or incorrect if the diff or repository context is missing. <br>
Mitigation: Verify important findings against the actual diff, tests, and repository conventions before acting on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review with ordered findings, risk summary, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to be grounded in the actual pull request diff and prioritized by risk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
