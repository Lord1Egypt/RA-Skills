## Description:

Nightly Workspace Audit scans workspace files for dependency issues, manages HOT/WARM/COLD memory tiers, detects orphaned files and sync inconsistencies, and reports workspace health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emrys-hong](https://clawhub.ai/user/emrys-hong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to audit OpenClaw workspaces, identify broken links, orphaned files, duplicate or drifting memory content, and summarize cleanup or tier changes after nightly or manual checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad workspace and memory context during dependency discovery and memory hygiene checks.

Mitigation: Run it only in workspaces where that level of access is acceptable, and review the audit report before relying on its conclusions.

Risk: The skill can propose or perform persistent cleanup actions such as pruning, archiving, renaming, or MEMORY.md updates.

Mitigation: Use report-only or manual review first, keep backups or version control, and approve deletions, moves, renames, and memory edits before applying them.

Risk: Automatic HOT/WARM/COLD tier changes can remove frequently loaded context or archive useful memory if reference counts are incomplete.

Mitigation: Check listed promotions and demotions against cron jobs, local overrides, active projects, and recent workspace usage before accepting tier changes.

## Reference(s):

- [Tier Rules](references/tier-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/emrys-hong/skills/nightly-workspace-audit)
- [Publisher Profile](https://clawhub.ai/user/emrys-hong)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown health report with dependency, cleanup, tier-change, sync, and health sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed or completed file cleanup, archive, rename, MEMORY.md update, and tier promotion or demotion details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
