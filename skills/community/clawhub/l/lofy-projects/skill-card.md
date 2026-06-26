## Description: <br>
Project management for the Lofy AI assistant - tracks multiple projects with milestones, priority scoring, meeting prep automation, time logging, stale project alerts, and work session recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to manage projects, coursework, and research by tracking status, deadlines, blockers, milestones, meetings, and time logs. It also helps prioritize work sessions and prepare concise meeting context from stored project data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist project changes to a local project tracker after project conversations. <br>
Mitigation: Require explicit confirmation before any JSON write, including a visible summary of the proposed change. <br>
Risk: The skill can proactively send meeting prep from broad meeting-related triggers. <br>
Mitigation: Require confirmation before sending meeting prep, including the destination and message summary. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose updates to a local data/projects.json tracker and meeting-prep messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
