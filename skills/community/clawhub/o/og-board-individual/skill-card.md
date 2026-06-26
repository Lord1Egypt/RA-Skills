## Description: <br>
Use when you need to work with tasks: view tasks, list tasks, update task status, add blockers, artifacts, and worklogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jatin-31](https://clawhub.ai/user/jatin-31) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to review assigned OpenGoat tasks and keep task status, blockers, artifacts, and worklogs current for a chosen agent ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Updating the wrong task or acting as the wrong agent could make task-board state inaccurate. <br>
Mitigation: Confirm the agent ID and task ID before making updates. <br>
Risk: Task notes, blockers, artifacts, or worklogs could expose secrets or sensitive internal details. <br>
Mitigation: Keep sensitive information out of free-text task fields and record only necessary operational context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jatin-31/og-board-individual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses task IDs, agent IDs, status values, and free-text notes supplied by the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
