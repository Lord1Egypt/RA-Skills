## Description: <br>
Run iterative agent loops until success criteria are met. Controlled autonomous iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Loop to repeat clearly scoped tasks, verify success criteria, and preserve concise iteration learnings until success or a bounded stopping condition is reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repeated attempts can amplify an incorrect plan or repeatedly propose risky commands. <br>
Mitigation: Keep success criteria narrow, review commands before they run, require explicit approval for destructive operations, and stop at the skill's bounded iteration limit. <br>
Risk: Loop history is saved locally under ~/loop/ and could contain sensitive task notes if the user includes them. <br>
Mitigation: Avoid putting secrets or sensitive data in loop notes, and review or delete local history when it is no longer needed. <br>
Risk: Autonomous iteration can increase token and tool-use cost. <br>
Mitigation: Estimate cost before starting, use a small iteration limit by default, and switch approaches instead of continuing when repeated attempts show the same failure pattern. <br>


## Reference(s): <br>
- [Loop on ClawHub](https://clawhub.ai/ivangdavila/loop) <br>
- [Publisher profile: ivangdavila](https://clawhub.ai/user/ivangdavila) <br>
- [Loop examples](examples.md) <br>
- [Memory between iterations](memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local loop state under ~/loop/ and record bounded iteration history.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
