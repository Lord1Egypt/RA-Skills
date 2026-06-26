## Description: <br>
Search, discover, and install skills from the open agent skills ecosystem to extend an agent for specific tasks or domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isainazar](https://clawhub.ai/user/isainazar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when a user needs a specialized capability and an existing skill may already cover the task. It guides the agent to search the skill ecosystem, present candidate skills, and offer installation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer ordinary help requests toward third-party skill installation. <br>
Mitigation: Use it only when the user explicitly wants skill discovery or when a skill search is clearly relevant; present options for review before installation. <br>
Risk: The artifact recommends global, auto-confirmed installation commands. <br>
Mitigation: Review the skill source and publisher before installing, avoid auto-confirmed global installs, and prefer scoped installs with a clear rollback path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isainazar/openclaw-find-skills) <br>
- [Skills catalog](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose third-party skill installation commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
