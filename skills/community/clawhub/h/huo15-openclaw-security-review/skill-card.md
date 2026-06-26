## Description: <br>
Reviews pending repository changes for secrets, injection, XSS, SSRF, authorization bypass, and risky dependency patterns, then reports severity and remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before PR merges, public releases, or incident follow-up to statically review repository changes for common vulnerability classes and receive severity-ranked findings with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review requires reading repository diffs and may inspect git history, which can expose secrets or sensitive code. <br>
Mitigation: Install only in repositories where that access is acceptable, and keep generated reports redacted. <br>
Risk: Static pattern matching can miss vulnerabilities or report false positives. <br>
Mitigation: Treat findings as review guidance and confirm them against the affected code before merging or releasing. <br>
Risk: Remediation advice can involve credentials, git history, or dependency updates. <br>
Mitigation: Keep remediation user-controlled; do not automatically revoke keys, rewrite history, or force dependency updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-security-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security review report with severity-ranked findings, CWE mappings, remediation guidance, and optional user-run shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secrets are redacted; destructive remediation such as key revocation, history rewriting, and forced dependency updates remains user-controlled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
