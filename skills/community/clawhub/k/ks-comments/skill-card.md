## Description:

Collect public Kuaishou video comments and replies in user-approved steps, then review incremental results or export them as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users can collect public Kuaishou video comments and replies one user-approved step at a time, review the results, and export collected comments to CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports account-token exposure.

Mitigation: Keep account tokens private and restrict access to the local configuration file; revoke or rotate a token if exposure is suspected.

Risk: The default service address uses plain HTTP, and the security summary also reports insecure TLS support.

Mitigation: Use an HTTPS service endpoint with certificate verification enabled; do not enable insecure TLS for routine use.

Risk: ClawScan reports capabilities beyond the stated collection purpose, and its analysis is incomplete.

Mitigation: Review the full skill and its components before use, and limit use to the stated task until the broader capabilities are understood.

## Reference(s):

- [ks-comments on ClawHub](https://clawhub.ai/mystery77777777/skills/ks-comments)
- [Publisher profile](https://clawhub.ai/user/mystery77777777)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Shell commands, Configuration instructions, User guidance]

**Output Format:** [JSON results, CSV comment exports, and concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incremental, session-based results; CSV exports include a BOM for spreadsheet compatibility.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
