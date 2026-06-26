## Description: <br>
Hierarchical persistent planning for complex multi-phase tasks that asks an agent to create and maintain structured .plan files, re-read current planning context, and save key milestones for cross-session continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noirewinter](https://clawhub.ai/user/noirewinter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use hplan to break complex, multi-phase tasks into persistent plans, phase specifications, checklists, decision logs, and progress records. It is intended for work that benefits from explicit planning, confirmation, and continuity across long or interrupted sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores task goals, phase details, decisions, and progress in workspace files and may save summaries to long-term memory. <br>
Mitigation: Avoid using it for confidential or audit-sensitive work unless that persistence is acceptable, and review generated plan and memory content before sharing the workspace. <br>
Risk: The skill can delete a completed .plan/ directory without explicit user control. <br>
Mitigation: Retain or archive completed .plan/ directories before installing or adapt the skill instructions to request approval before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noirewinter/hplan) <br>
- [Publisher profile](https://clawhub.ai/user/noirewinter) <br>
- [Project homepage](https://github.com/Noirewinter/hplan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates .plan/ planning files and may save task summaries to long-term memory when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
