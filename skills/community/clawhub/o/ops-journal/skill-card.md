## Description: <br>
Automates logging of deployments, incidents, changes, and decisions into a searchable local operations journal with incident timelines and postmortem-ready exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and incident responders use this skill to record operational events, manage incidents, search journal history, and generate summaries or exports for handoff and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal entries and incident reports may contain sensitive operational details. <br>
Mitigation: Do not log passwords, tokens, private keys, regulated data, or other secrets; protect the journal directory before deployment. <br>
Risk: Timeline and export commands can write files to paths supplied by the user. <br>
Mitigation: Use output paths carefully and review exported Markdown, JSON, or CSV files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/ops-journal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Terminal text plus optional JSON, Markdown, and CSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists entries in a local SQLite journal and can write timeline or export files to user-provided output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
