## Description: <br>
An adaptive proactive agent skill that manages user energy levels and task prioritization using semantic pulse checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adnxone](https://clawhub.ai/user/adnxone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to let an agent adapt task suggestions, nudges, and recovery-oriented guidance based on inferred user energy and explicit /pulse commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may infer energy, availability, or related personal state from conversation context and configured files. <br>
Mitigation: Keep CONTEXT_SOURCES limited to specific, low-sensitivity files and avoid journals, logs, or health-related notes unless that use is intentional. <br>
Risk: Proactive nudges may become unwanted or disruptive. <br>
Mitigation: Use /pulse quiet or disable the skill when nudges are not desired, and review pulse state/history files periodically. <br>


## Reference(s): <br>
- [NXT Pulse Agent on ClawHub](https://clawhub.ai/adnxone/nxt-pulse-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status output and Markdown guidance with JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local pulse state and history files under memory/ when the pulse script runs.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
