## Description:

GitGuard gives agents repo-auditing tools for local secret scanning, composite repository health scoring, commit quality analysis, stale branch review, dependency freshness checks, and optional GitHub PR or issue triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use GitGuard to audit their own Git repositories for exposed secrets, repository health, commit hygiene, stale branches, dependency freshness, and GitHub backlog triage. It is intended for defensive maintenance of repositories the user owns or is authorized to inspect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret scanning can follow repository symlinks and read files outside the selected repo, weakening local-scope assumptions.

Mitigation: Inspect untrusted repositories for symlinks before scanning and run GitGuard only against repositories you own or trust.

Risk: Dependency freshness and GitHub triage can disclose dependency names or repository identifiers to external services when those checks are enabled.

Mitigation: Prefer offline local checks when disclosure is not acceptable, and use a minimally scoped GitHub token for authenticated GitHub triage.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/welove111/skills/gitguard-skill)
- [Publisher Profile](https://clawhub.ai/user/welove111)
- [Project Website](https://btc-vision.org)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise text summaries and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret findings are described with redacted previews; dependency freshness and GitHub triage can use optional read-only network requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
