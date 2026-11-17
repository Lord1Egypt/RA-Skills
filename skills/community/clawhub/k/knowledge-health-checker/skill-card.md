## Description:

Audit and improve Markdown knowledge-base health across Obsidian, Logseq, Notion exports, docs folders, and wiki repositories by detecting empty placeholder notes, broken wiki links, weak content density, orphan notes, graph fragmentation, stale files, and repair opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xb19960921](https://clawhub.ai/user/xb19960921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and knowledge-base maintainers use this skill to audit Markdown vaults and documentation folders for structural health, broken links, hollow notes, density issues, and graph connectivity. It produces prioritized findings and reviewed fix plans for safer maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated repair scripts can delete or rewrite knowledge-base files.

Mitigation: Use scan and report modes first, review generated scripts manually, and keep backups before running any repair script.

Risk: Unsafe input handling can affect generated repair scripts or reports when processing untrusted results JSON or knowledge bases.

Mitigation: Run the skill only on trusted local Markdown folders and trusted scan results until path validation, repair-script generation, and HTML escaping concerns are fixed.

Risk: The auto-fix path may be mistaken for a safe dry run.

Mitigation: Treat auto_fix.py output as executable code requiring human review rather than as a harmless preview.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xb19960921/skills/knowledge-health-checker)
- [Publisher profile](https://clawhub.ai/user/xb19960921)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON scan results, HTML reports, and generated shell or Python fix scripts when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default posture is report and propose; destructive file changes require explicit review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
