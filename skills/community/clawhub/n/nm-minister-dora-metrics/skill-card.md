## Description: <br>
Computes DORA delivery-performance metrics from git and GitHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and release reviewers use this skill to compute DORA delivery metrics from repository and GitHub data, classify delivery performance, and identify the weakest improvement area. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow analyzes git history and GitHub delivery metadata, which may expose sensitive repository, issue, or pull request information to the local agent workflow. <br>
Mitigation: Run it only on repositories where that metadata exposure is acceptable, and review local data-handling expectations before use. <br>
Risk: Broad trigger terms could activate the skill in contexts where DORA analysis is not intended. <br>
Mitigation: Narrow or customize triggers when accidental activation would disrupt normal repository work. <br>
Risk: DORA classifications depend on repository release cadence, production branch selection, and failure labeling quality. <br>
Mitigation: Verify the selected branch and failure label, rerun over a narrower window, and sample contributing GitHub issues before using results for management decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-minister-dora-metrics) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/minister) <br>
- [kuva plotting reference](https://github.com/Psy-Fer/kuva) <br>
- [Agentic Workflow Signals from DORA](modules/agentic-workflow-signals.md) <br>
- [DORA Tier Thresholds](modules/thresholds.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON report descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-metric values, tier classifications, an overall tier, and a bottleneck pointer.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
