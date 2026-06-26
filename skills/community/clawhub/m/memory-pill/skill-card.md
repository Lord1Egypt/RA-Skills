## Description: <br>
Memory Pill is an AI-native memory and orchestration system for OpenClaw that helps agents use persistent memory, behavioral discipline, and delegation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7D-codes](https://clawhub.ai/user/7D-codes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to initialize and maintain persistent workspace memory, project notes, daily notes, behavior files, and orchestration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent local memory and behavior files under ~/.openclaw/workspace. <br>
Mitigation: Review planned diffs before activation, periodically inspect the workspace, and avoid storing secrets or sensitive personal data. <br>
Risk: Email, calendar, and cron-related checks are described as optional behaviors. <br>
Mitigation: Treat those integrations as separate opt-in actions and confirm scope before enabling scheduled or external checks. <br>


## Reference(s): <br>
- [Memory Pill on ClawHub](https://clawhub.ai/7D-codes/memory-pill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to ~/.openclaw/workspace and related behavior files; activation asks the user before setup.] <br>

## Skill Version(s): <br>
0.8.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
