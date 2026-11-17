## Description:

Research a sector and produce a source-cited industry report with market analysis, representative product comparisons, barriers, and evidence gaps, retaining the research and revisions in JishuDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and decision-makers use this skill to turn a sector name into a written, cited industry brief with a product comparison and documented information gaps. It saves report files locally and retains evidence and revisions in an authorized JishuDB knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled JishuDB setup can install software, download installer assets, change local configuration, and retain research records.

Mitigation: Review the setup plan and grant installation, connector, and data-retention permissions only for the intended machine and knowledge base.

Risk: The Windows helper invokes PowerShell for shortcut creation despite documentation saying PowerShell should not be invoked.

Mitigation: Review the Windows helper and its PowerShell use before running installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-aijishu/skills/industry-report-sprint)
- [Project homepage](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/industry-report-sprint)
- [Report discovery and evidence contract](references/evidence-contract.md)
- [JishuDB setup quickstart](references/jishudb-setup/references/setup-quickstart.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV]

**Output Format:** [Markdown report, comparison matrix, source and revision files, and evidence CSV; retained JishuDB records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Citations, evidence coverage, and unresolved information gaps]

## Skill Version(s):

0.1.17 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
