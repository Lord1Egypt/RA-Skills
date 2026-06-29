## Description: <br>
Detects workflow failures and inefficient patterns then files GitHub issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to monitor workflow executions, detect failures or efficiency problems, and prepare or create repository issues with evidence and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue bodies may expose secrets, private command output, or sensitive workflow logs if raw evidence is posted without review. <br>
Mitigation: Review and redact issue content before posting; keep automatic issue creation disabled unless intentional. <br>
Risk: Repository credentials used for issue creation could grant broader access than the skill needs. <br>
Mitigation: Use credentials limited to issue management for the target repository or project. <br>
Risk: Automatic reporting can create noisy or duplicate issues. <br>
Mitigation: Use duplicate checks, severity thresholds, rate limits, and human approval before creating issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-workflow-monitor) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Detection Patterns](artifact/modules/detection-patterns.md) <br>
- [Efficiency Metrics](artifact/modules/efficiency-metrics.md) <br>
- [Issue Templates](artifact/modules/issue-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, issue drafts, shell command snippets, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May draft or create GitHub/GitLab issues when configured; default configuration requires approval before issue creation.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
