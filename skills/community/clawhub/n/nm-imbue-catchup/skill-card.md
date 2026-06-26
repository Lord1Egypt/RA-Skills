## Description: <br>
Summarizes recent git changes for context recovery after session breaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and project collaborators use this skill to get up to speed after a session break, handoff, or absence by summarizing recent changes, key implications, follow-ups, and blockers across git repositories, notes, tickets, documents, or logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad catchup or status requests and inspect repositories, notes, issue trackers, or logs that the user points it at. <br>
Mitigation: Set explicit scope, baseline, time window, and allowed data sources before analysis begins. <br>
Risk: Logs, documents, or notes used for catchup may contain sensitive information. <br>
Mitigation: Limit analysis to necessary files or systems and summarize patterns instead of reproducing sensitive raw content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/athola/nm-imbue-catchup) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with headings, bullets, checklists, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for scoped catchup summaries with concise references to source paths, lines, time windows, and follow-up actions.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
