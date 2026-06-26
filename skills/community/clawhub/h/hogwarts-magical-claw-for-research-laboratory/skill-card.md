## Description: <br>
A research team collaboration agent that manages team knowledge, tracks project progress, assists with meeting notes, literature reviews, experiment records, code, and data analysis, and follows daily and weekly coordination protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Research teams use this skill to coordinate meetings, summarize decisions, track milestones and blockers, maintain team knowledge, and support documentation, code, and data-analysis tasks. It is intended for team workspaces where members can explicitly opt in to automated reminders and status tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring monitoring and chat reminders can expose member availability, workload, blockers, or unpublished research details. <br>
Mitigation: Enable the skill only in opt-in team workspaces, restrict approved channels and mention targets, and define what member records and project details may be read, retained, or posted. <br>
Risk: The skill can generate public or semi-public notifications about blockers, security issues, protected data, or sensitive research. <br>
Mitigation: Require human approval before posting sensitive blockers, security issues, protected data, unpublished findings, or escalation messages outside approved private channels. <br>
Risk: Workspace file updates for logs, plans, summaries, and knowledge-base records may alter shared team documentation. <br>
Mitigation: Limit write permissions to approved paths, require review for shared team files, and keep Git commits auditable so changes can be inspected and reverted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biociao/hogwarts-magical-claw-for-research-laboratory) <br>
- [OpenClaw research team collaboration protocol](artifact/references/protocol.md) <br>
- [Team Git repository referenced by artifact](https://gitea.biochao.cc/BioChaoGroup/ClawNotes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with tables, task lists, summaries, code blocks, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace files for meeting notes, progress logs, knowledge-base summaries, task plans, human-in-the-loop requests, and Git commit guidance when explicitly authorized by the workspace protocol.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
