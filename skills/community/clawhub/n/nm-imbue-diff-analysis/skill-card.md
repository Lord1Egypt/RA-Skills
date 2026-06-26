## Description: <br>
Analyzes changesets with risk scoring, categorization by type and impact, and release note preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze diffs, migrations, changelogs, configuration changes, API changes, and document revisions before review or release. It helps establish a baseline, categorize changes, assess impact and risk, and prepare summaries such as release notes or changelog entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger words such as changes or impact may activate the skill more often than expected. <br>
Mitigation: Confirm the analysis scope before applying the workflow and use it when structured change analysis is actually needed. <br>
Risk: Separate Night Market or Claude Code plugin installation is outside the markdown skill artifact reviewed here. <br>
Mitigation: Review any related plugin installation independently before enabling additional agents, hooks, commands, or configuration. <br>
Risk: Change-analysis summaries can influence release or review decisions if they are incomplete or incorrect. <br>
Mitigation: Review generated categories, risk ratings, and release notes against the underlying diff before using them downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-diff-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional inline shell commands and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces change categories, risk assessments, review focus areas, dependencies, and release-ready summaries.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
