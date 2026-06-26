## Description: <br>
Automates weekday Blue World Marketing morning standups by parsing Slack discussion, delegating tasks to AI agents, saving meeting memory, and reporting a summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Blue World Marketing teams use this skill to process daily Slack standups, extract assignments, route work to relevant AI agents, and maintain meeting and task records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack conversations can trigger recurring storage, task delegation, and cross-agent business actions without clear approval limits. <br>
Mitigation: Set explicit Slack channel scopes, participant notice, retention rules, and human approval gates before enabling automated action. <br>
Risk: Delegated tasks may post externally or affect financial, order, code, infrastructure, customer, or support content. <br>
Mitigation: Require human confirmation before any task posts externally or changes sensitive business systems or customer-facing content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/morning-meeting-bwm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, Slack summary text, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create dated meeting summaries and task status files under the configured memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
