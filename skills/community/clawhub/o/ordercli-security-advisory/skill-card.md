## Description: <br>
Security advisory for OrderCLI: 2 high/critical issues found on 2026-05-07T09:15:31Z. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this advisory to understand reported OrderCLI audit findings and recommended remediation before relying on that project in an environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advisory may not match a user's local OrderCLI path or current audit results. <br>
Mitigation: Verify the referenced path and audit findings against the local environment before acting on the recommendations. <br>
Risk: The advisory references a local audit script that could behave differently in another environment. <br>
Mitigation: Inspect any local run-audit.sh script before running it, then rerun the audit after remediation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/ordercli-security-advisory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown advisory with findings and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only advisory; does not run commands or request access to user data.] <br>

## Skill Version(s): <br>
0.1.202605071715 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
