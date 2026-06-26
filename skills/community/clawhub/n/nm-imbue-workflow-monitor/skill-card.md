## Description: <br>
Detects workflow failures and inefficient patterns then files GitHub issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor workflow executions for command failures, timeouts, retry loops, context exhaustion, and inefficient tool usage, then produce evidence-backed issue reports and improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed git diffs and selected repo-relative evidence may be sent to a configured reviewer provider. <br>
Mitigation: Review secret-bearing changes before use, and use narrower reviewer, engine, or web-search settings for private or sensitive repositories. <br>
Risk: Automatically generated issue reports may contain incorrect or incomplete analysis. <br>
Mitigation: Require human review of evidence, severity, and suggested fixes before filing or acting on issues. <br>
Risk: Issue creation can create noise or duplicates if enabled without controls. <br>
Mitigation: Keep approval required unless explicitly configured otherwise, check for duplicates, and retain rate limits before creating issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-workflow-monitor) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Detection Patterns](artifact/modules/detection-patterns.md) <br>
- [Efficiency Metrics](artifact/modules/efficiency-metrics.md) <br>
- [Issue Templates](artifact/modules/issue-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, issue templates, shell command examples, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include evidence summaries, efficiency scores, recommended fixes, and issue-creation prompts.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
