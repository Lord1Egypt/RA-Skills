## Description: <br>
Revenue-focused execution operating system for agents that converts "do it now" requests into immediate tool actions, enforces strict start/progress/finish SLAs, and prevents kickoff-only false completions for shipping tasks where delay kills conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rui131](https://clawhub.ai/user/rui131) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to make agents start execution-heavy publishing, release, distribution, and post-release tasks immediately, keep progress visible, and close with evidence-backed completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push agents to start tools, subagents, or cron work before approval boundaries are clear. <br>
Mitigation: Require confirmation before irreversible, externally visible, financial, account-changing, publishing, release, or destructive operations. <br>
Risk: The skill recommends KPI logging to memory and Obsidian daily notes. <br>
Mitigation: Use it only where persistent KPI records are acceptable, and disable or scope logging for sensitive environments. <br>
Risk: The skill directs agents to make permanent MISSION or skill updates after delays. <br>
Mitigation: Require review before persistent rule changes so execution pressure does not introduce unsuitable operating instructions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with status-message templates and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include KPI logging blocks and evidence pointers when the task is execution-heavy.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
