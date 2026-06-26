## Description: <br>
My Fitness Claw lets an OpenClaw agent log meals from natural language, estimate macros and micronutrients, update local nutrition records, and show progress in a dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Serg010101](https://clawhub.ai/user/Serg010101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to track personal nutrition by chatting with an agent that estimates intake, updates local logs, and presents daily progress. It is suited for personal food logging and dashboard-based nutrition review, not medical diagnosis or clinical nutrition advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal, nutrition target, and insight data can include personal health or diet information stored in workspace files and agent memory. <br>
Mitigation: Use only in workspaces where that storage is acceptable, and clear nutrition data, offline dashboard mirrors, and memory files before sharing or publishing. <br>
Risk: Micronutrient targets, estimates, and tips are generic and may be inaccurate for a specific person. <br>
Mitigation: Treat nutrition outputs as estimates and verify diet or supplement decisions with appropriate professional guidance. <br>
Risk: Serving the workspace from its root can expose more local files than the dashboard requires. <br>
Mitigation: Prefer opening the offline dashboard file directly, or serve only the minimum dashboard directory when browser hosting is necessary. <br>


## Reference(s): <br>
- [My Fitness Claw on ClawHub](https://clawhub.ai/Serg010101/my-fitness-claw) <br>
- [Serg010101 Publisher Profile](https://clawhub.ai/user/Serg010101) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chat text plus local JSON nutrition logs, Markdown memory entries, dashboard data, and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates workspace nutrition files and an offline dashboard data mirror.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
