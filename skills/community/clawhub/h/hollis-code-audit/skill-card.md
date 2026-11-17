## Description:

Code Audit guides agents through read-only, evidence-backed audits of repositories, pull requests, security risks, regressions, and intent alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to run artifact-focused code audits, security reviews, regression-risk reviews, and intent-alignment checks. It helps agents read project intent first, inspect relevant code and tests, disclose independent-review limitations, and report prioritized findings with evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect repository structure, git metadata, selected files, and diffs.

Mitigation: Use it only in repositories where that inspection is appropriate, and configure skip patterns or .auditignore entries for generated, noisy, or confidential paths.

Risk: External model or subagent review can expose sensitive code or unreleased business context if a diff or audit packet is shared too broadly.

Mitigation: Check project confidentiality rules first, redact sensitive material, and include full diffs only when they are safe to share.

Risk: Independent review may be unavailable or may use a correlated model, leaving shared blind spots.

Mitigation: Disclose the independent-review status in the audit report and seek a strong non-current-model or human second pass for high-stakes decisions.

## Reference(s):

- [Code Audit Skill README](README.md)
- [Audit Checklist](references/audit-checklist.md)
- [Independent Reviewer Prompt](references/independent-reviewer-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/hollis9087/skills/hollis-code-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports with optional JSON helper-script output and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce compact audit packets and reviewer-route inventories; helper scripts are optional and use the Python standard library.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
