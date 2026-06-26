## Description: <br>
InspirAI Evo detects workflow problem signals such as repeated trial and error, interrupted flows, and git churn, then generates analysis reports and guides improvement handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review agent workflow signals, produce concise evolution reports, and queue follow-up improvements without blocking the current task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reports and state files may contain sensitive project context if shared or committed. <br>
Mitigation: Review docs/evo-reports, .evo-state.json, and ~/.claude/evo-stats before sharing or committing, and delete stored state when it is no longer needed. <br>
Risk: Optional automatic monitoring can persist signal history across future sessions. <br>
Mitigation: Add the CLAUDE.md monitoring block only when persistent tracking is desired, and periodically review or remove generated history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexxxiong/inspirai-evo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project reports, project state, and optional cross-project statistics when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
