## Description: <br>
Audits JWT and OAuth/OIDC token security locally by decoding claims and scanning code or environment files for insecure token handling patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect JWTs, OAuth scopes, and source files for token handling risks before deployment or during authentication reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect JWTs, OAuth scopes, source files, and .env files that contain sensitive tokens or credentials. <br>
Mitigation: Use expired or test tokens where possible, scope scans to the smallest relevant directory, and redact or rotate any live credentials that appear in output. <br>
Risk: Audit reports can include decoded claims, file paths, line numbers, and remediation snippets that may expose sensitive implementation details if shared broadly. <br>
Mitigation: Review and sanitize reports before sharing them outside the team or attaching them to tickets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PHY041/phy-jwt-auth-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown security report with severity-ranked findings, code locations, and remediation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include decoded JWT claims, source paths, line numbers, and concrete fixes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
