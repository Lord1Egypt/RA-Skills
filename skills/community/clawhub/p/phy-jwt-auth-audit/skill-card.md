## Description:

Audits JWT and OAuth/OIDC token security locally by decoding claims, scanning source and .env files for insecure token handling, and producing severity-ranked findings with fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to review JWT, OAuth, and OIDC token handling in application code, token samples, and intended .env files. It helps identify risky claims, insecure storage or logging patterns, broad scopes, weak secrets, and missing validation controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan credential-bearing .env files and may include weak secret values or token-derived details in reports.

Mitigation: Run it only on repositories and env files intended for audit, restrict report access, and rotate any real secret that appears in output.

Risk: Broad workspace scans can collect sensitive findings from files outside the intended review scope.

Mitigation: Use targeted paths for scans and review generated findings before sharing or storing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-jwt-auth-audit)
- [Publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown security audit report with severity-ranked findings, code locations, and remediation snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decoded token claims, paths, line numbers, and secret-like values found in audited inputs.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
