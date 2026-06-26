## Description: <br>
Audits code for security issues including sensitive data exposure, dependency vulnerabilities, SQL injection, and hardcoded secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to perform security reviews before deployment, third-party adoption, or periodic code audits. It focuses the review on secrets, vulnerable dependencies, injection risks, authorization, and unsafe logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested local scans can surface secrets or sensitive findings in terminal output or audit notes. <br>
Mitigation: Confirm the target directory before scanning and avoid sharing any secrets discovered during review. <br>
Risk: Dependency scan commands may require installing or running local audit tools. <br>
Mitigation: Review commands before execution and run them in an appropriate project environment with normal least-privilege safeguards. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown security audit report with checklist items and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity sections, remediation guidance, and passed-check summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
