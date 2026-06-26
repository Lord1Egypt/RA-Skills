## Description: <br>
Track and log progress on long-term goals with daily updates, milestone marking, MRR tracking, and weekly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alti-Systems](https://clawhub.ai/user/Alti-Systems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals, operators, and agents use this skill to maintain accountability for long-term training and business goals by logging daily activity, updating revenue progress, marking milestones, and reviewing weekly status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes local tools at /root/clawd/tracker and /root/clawd/goal-tracker/generate-dashboard. <br>
Mitigation: Before installing or running the skill, verify those paths resolve to the trusted local tracker tools expected for this release. <br>
Risk: Goal logs, dashboard output, and revenue updates may contain private training habits, business wins, or MRR figures. <br>
Mitigation: Keep generated dashboard and data files private, and avoid sharing logs or screenshots unless they have been reviewed for sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alti-Systems/goal-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local tracker commands and may update local goal data, daily logs, MRR records, milestone state, weekly summaries, and an HTML dashboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
