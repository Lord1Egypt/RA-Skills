## Description: <br>
Audit and improve Markdown knowledge-base health across Obsidian, Logseq, Notion exports, docs folders, and wiki repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and knowledge-base owners use this skill to scan Markdown vaults, docs folders, and wiki exports for hollow notes, broken links, stale files, weak density, orphan notes, and graph fragmentation. It helps produce prioritized health reports and safe fix plans before cleanup or migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local Markdown folders and may write report or fix-plan artifacts. <br>
Mitigation: Run it only against intended knowledge-base paths and review generated artifacts before relying on them. <br>
Risk: Generated HTML reports or repair scripts may reflect attacker-controlled paths or propose destructive changes such as deletes, renames, or link rewrites. <br>
Mitigation: Open generated reports cautiously and inspect any repair script before execution; require explicit confirmation before destructive or global changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xb19960921/knowledge-health-checker) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [Test prompts](artifact/test-prompts.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, health summaries, prioritized fix plans, and optional JSON, HTML, or repair-script artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only by default; generated fix scripts and local artifacts require review before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
