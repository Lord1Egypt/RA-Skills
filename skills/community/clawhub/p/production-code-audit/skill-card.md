## Description: <br>
Deep-scan a codebase, understand its architecture and patterns, then produce a comprehensive audit report with prioritized fixes. Optionally apply changes on a feature branch with a PR for review. Covers security, performance, error handling, logging, testing, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit a codebase for production readiness across security, performance, architecture, testing, logging, and documentation. In its default posture it produces a read-only report; when explicitly requested, it may propose or apply fixes on a dedicated review branch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move beyond analysis into code changes, test execution, branch workflow, and pull request actions. <br>
Mitigation: Use audit-only mode by default, require explicit approval before fix mode, and review all changes before merge. <br>
Risk: Security or secret findings may expose sensitive file locations or tempt automatic secret edits. <br>
Mitigation: Flag secrets without logging values, rotate affected credentials outside the agent workflow, and avoid automatic secret removal or commits. <br>
Risk: Generated fixes or broad production-readiness recommendations may be incorrect for the target system. <br>
Mitigation: Run changes in a disposable branch or sandbox, review findings with maintainers, and execute tests only in approved sandboxed or CI environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/production-code-audit) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>
- [Google Engineering Practices](https://google.github.io/eng-practices/) <br>
- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/) <br>
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit report with prioritized findings, optional code diffs, and review workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default mode is read-only audit reporting; fix mode may create branches, modify files, run tests, and prepare pull request guidance when explicitly requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
