## Description:

Kai Report Creator generates bilingual, single-file HTML reports, business summaries, research documents, and KPI dashboards from notes, data, URLs, or .report.md plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and knowledge workers use this skill to turn raw notes, data, URLs, or approved report plans into polished bilingual HTML reports. It also supports report review, theme previews, offline bundling, and optional image export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can load mutable third-party browser scripts when not bundled for offline use.

Mitigation: Use offline bundling where practical, verify generated HTML before opening confidential reports, and review any external script loading before sharing.

Risk: Report content may be sent to Telegram or another messaging channel after image export.

Mitigation: Require explicit user confirmation of the destination and review the rendered report or image before any messaging send.

Risk: Generated reports can mislead readers if source data is incomplete or placeholders remain.

Mitigation: Check generated facts, KPI values, and placeholders before publication; missing values should remain visibly marked rather than being invented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaisersong/skills/kai-report-creator)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Reference index](artifact/references/INDEX.md)
- [HTML shell contract](artifact/references/html-shell-template.md)
- [IR contract](artifact/references/ir-contract.md)
- [Generated guide example](https://kaisersong.github.io/kai-report-creator/examples/zh/kai-report-creator-guide.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans, .report.md intermediate representations, self-contained HTML files, review notes, and optional export commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML can embed report-summary JSON, section summaries, component data, theme metadata, and export controls.]

## Skill Version(s):

1.23.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
