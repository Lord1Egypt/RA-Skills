## Description:

Pharmaziegasse is a namespace skill for Netsnek e.U.'s pharmacy management platform, covering prescription tracking, inventory, compliance, and staff coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve concise information about Pharmaziegasse modules and platform metadata for DACH-region pharmacy workflows.

### Deployment Geography for Use:

DACH region (Austria, Germany, Switzerland)

## Known Risks and Mitigations:

Risk: The skill grants exec permission for a bundled information script.

Mitigation: Review the local script before installation; users who avoid shell-capable skills can decline installation or request a markdown-only package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/pharmaziegasse)
- [Netsnek e.U.](https://netsnek.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON from a local shell script, summarized in Markdown when answering users]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux exec permission for scripts/pharma-info.sh; no credentials or hidden data access were identified in the server security evidence.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
