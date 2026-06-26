## Description: <br>
Tokens tell you how much you paid. Tasks tell you what you got. Tally tracks every OpenClaw task from start to finish -- cost, complexity, and efficiency score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use OpenClaw Tally to track OpenClaw tasks, token costs, task complexity, and task efficiency scores through a local analytics ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The message-post hook reads every OpenClaw message to classify task activity. <br>
Mitigation: Install only where local message inspection is acceptable, and review the security declaration before enabling the hook. <br>
Risk: The local SQLite database can reveal sessions, models, costs, task history, and potentially high-level task summaries. <br>
Mitigation: Treat ~/.openclaw/tally/tally.db as private local data and apply normal workstation access controls and backup hygiene. <br>


## Reference(s): <br>
- [OpenClaw Tally on ClawHub](https://clawhub.ai/JonathanJing/openclaw-tally) <br>
- [Publisher profile](https://clawhub.ai/user/JonathanJing) <br>
- [README](README.md) <br>
- [Product requirements document](PRD.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-style task analytics responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task and cost metadata locally in SQLite under ~/.openclaw/tally/.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
