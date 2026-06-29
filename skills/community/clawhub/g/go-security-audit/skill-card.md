## Description: <br>
Performs a security audit of a Go codebase, focusing on concurrency bugs, resource leaks, error handling gaps, command injection, and authentication bypasses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forgou37](https://clawhub.ai/user/forgou37) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review Go repositories for security and reliability issues and to produce prioritized findings with file and line citations plus minimal patch suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested audit findings or patches may be incorrect or incomplete for a target repository. <br>
Mitigation: Review findings and proposed patches before applying them, and validate changes with the repository's normal test and security review process. <br>
Risk: The skill is intended to inspect Go repository code when explicitly used for an audit. <br>
Mitigation: Run it only on repositories the user is authorized to review and limit shared context to code needed for the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forgou37/go-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/forgou37) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown findings with file:line citations and Go code blocks for suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritized by severity from critical through low] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
