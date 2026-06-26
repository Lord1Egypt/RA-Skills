## Description: <br>
Auto-analyze mistake and success patterns and reflect in skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to summarize mistakes, successes, and performance observations into reusable learned rules, reports, events, and proposed updates to related skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist learned content from local memory files and propose changes to other skills. <br>
Mitigation: Require manual approval with visible diffs before applying any skill-file update. <br>
Risk: Sensitive information from error logs, self-evaluations, or performance notes could be included in generated learning artifacts. <br>
Mitigation: Redact sensitive log content before generating or storing learned rules, reports, or events. <br>
Risk: Automatically generated learning artifacts can accumulate outdated or incorrect guidance. <br>
Mitigation: Keep backups, set retention limits, and review generated rules before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/learning-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style guidance for learned rules, learning reports, events, and skill updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persisted learning artifacts and changes to other skill files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
