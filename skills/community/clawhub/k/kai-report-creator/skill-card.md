## Description: <br>
Creates bilingual single-file HTML reports, business summaries, dashboards, and research documents from notes, URLs, or `.report.md` intermediate representations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to plan, generate, review, theme, and optionally export async-friendly HTML reports from source material or approved report IR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports can load third-party CDN JavaScript when assets are not bundled or used offline. <br>
Mitigation: Open sensitive reports without network access, or use the bundled/offline path when third-party dependencies are not trusted. <br>
Risk: Report files include local edit and export controls that can affect the viewed or shared output. <br>
Mitigation: Review generated reports before distribution and keep trusted copies of source `.report.md` IR or generated HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/kai-report-creator) <br>
- [Generated guide report](https://kaisersong.github.io/kai-report-creator/examples/zh/kai-report-creator-guide.html) <br>
- [References index](artifact/references/INDEX.md) <br>
- [Report IR contract](artifact/references/ir-contract.md) <br>
- [HTML shell template](artifact/references/html-shell-template.md) <br>
- [Review checklist](artifact/references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report IR, single-file HTML reports, review summaries, and optional image-export command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include local edit/export controls and either CDN or bundled assets depending on the selected path.] <br>

## Skill Version(s): <br>
1.23.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
