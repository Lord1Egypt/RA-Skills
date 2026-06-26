## Description: <br>
ITIL-aligned incident, problem, and change management for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chefboyrdave21](https://clawhub.ai/user/chefboyrdave21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to detect service crashes, cron failures, resource pressure, and data integrity issues, then classify incidents, identify recurring problems, assess changes, and track operational follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over services, cron jobs, configuration changes, and operational follow-up. <br>
Mitigation: Start in report-only mode, define the exact services and files in scope, and require explicit approval for restarts, configuration edits, cron changes, and other service-impacting actions. <br>
Risk: Recurring reviews inspect local logs, cron state, health endpoints, and agent memory or state files. <br>
Mitigation: Run scheduled reviews only in environments where that local operational inspection is intended, and scope filesystem and service access to the minimum needed for the review. <br>
Risk: The security evidence flags unsafe Python filename handling in the shell review script. <br>
Mitigation: Fix the filename handling before operational use or restrict execution to trusted paths and controlled job files until the script is hardened. <br>


## Reference(s): <br>
- [ITIL 4 Agent Operations Mapping](references/itil4-agent-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chefboyrdave21/itil-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured incident, problem, change, and health-review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce coordination-task templates, review reports, severity classifications, RCA prompts, change checklists, and operational follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
