## Description: <br>
Nightly Workspace Audit scans OpenClaw workspace Markdown and JSON files for dependency issues, memory hygiene needs, HOT/WARM/COLD tier changes, sync inconsistencies, and workspace health reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emrys-hong](https://clawhub.ai/user/emrys-hong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to run scheduled or requested OpenClaw workspace audits, identify broken links and orphaned files, manage memory tiers, and receive a concise health report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify persistent workspace memory by deleting, moving, renaming, archiving, or rewriting files during cleanup and tiering. <br>
Mitigation: Run a dry run first, keep backups of MEMORY.md and memory/, and require explicit approval before destructive or reorganizing changes. <br>
Risk: Automated dependency and tier decisions may misclassify useful files as orphaned, stale, or ready for demotion. <br>
Mitigation: Review the audit report and proposed tier changes before applying them, especially for cron-referenced, active project, or protected files. <br>


## Reference(s): <br>
- [Tier Rules](references/tier-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report with dependency, cleanup, tier-change, sync, and health sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include changed-file summaries and required review notes for memory tier changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
