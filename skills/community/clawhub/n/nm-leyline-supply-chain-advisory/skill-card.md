## Description:

Audits dependency supply chains for bad versions, lockfile drift, and artifact integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Python dependencies for known-bad versions, lockfile integrity issues, and suspicious installed artifacts. It also provides checklists and remediation guidance for suspected supply-chain incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The incident checklist captures the full environment in a temporary file, which may include credentials.

Mitigation: Avoid capturing the full environment; use a reviewed allowlist of needed values and redact secrets before saving any incident notes.

Risk: The security scan was partial, so its evidence does not cover several referenced files.

Mitigation: Review the referenced files and verify the guidance before relying on it for an incident response.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [ClawHub release](https://clawhub.ai/athola/skills/nm-leyline-supply-chain-advisory)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with checklists, shell commands, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations use project lockfiles, package versions, and known-bad version indicators as inputs.]

## Skill Version(s):

1.10.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
