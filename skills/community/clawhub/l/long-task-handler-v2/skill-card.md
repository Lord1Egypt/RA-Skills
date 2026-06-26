## Description: <br>
Long Task Handler V2 helps an agent estimate, background, monitor, and report progress for tasks expected to run longer than about 60 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrislawyeryounger-spec](https://clawhub.ai/user/chrislawyeryounger-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to keep long-running compile, deploy, training, migration, data-processing, crawling, and multi-step writing tasks visible through early estimates, periodic progress updates, completion notices, and transparent issue reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage backgrounding or delegating long-running tasks, which may reduce user visibility into active commands if the agent does not confirm the execution posture. <br>
Mitigation: Ask the agent to confirm before backgrounding tasks or using sub-agents, and require periodic progress updates for long-running work. <br>
Risk: The artifact's progress-message examples are primarily in Chinese, which may not match every user's preferred language. <br>
Mitigation: Request the preferred reporting language before relying on the skill's default status-message style. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrislawyeryounger-spec/long-task-handler-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown progress messages with optional shell-command handling and YAML-style configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses time estimates, quantified progress, reporting intervals, silent-task warnings, and completion status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
