## Description: <br>
Analyzes changesets with risk scoring, categorization by type and impact, and release note preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn raw changesets, git diffs, configuration changes, migrations, schema updates, or document revisions into categorized impact summaries, risk assessments, and release-note or changelog material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation keywords may cause the skill to load for generic change-related requests where a full PR review or security review is expected. <br>
Mitigation: Use this skill for summary-oriented diff impact analysis, and invoke a more specific review or security skill when the task requires full PR review or security review. <br>
Risk: Risk scores and summaries can miss context when the baseline, comparison scope, or supporting git data is incomplete. <br>
Mitigation: Establish the comparison baseline, gather diff statistics and relevant changed files first, then review the generated categorization and risk assessment before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-diff-analysis) <br>
- [claude-night-market imbue plugin](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [sem entity-level diff tool](https://github.com/Ataraxy-Labs/sem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with structured risk, categorization, and release-note sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include git command suggestions, categorized change lists, risk levels, mitigations, dependencies, and review focus areas.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
