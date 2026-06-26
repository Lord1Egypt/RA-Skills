## Description: <br>
Query Find My locations and battery status for family devices via iCloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liamnichols](https://clawhub.ai/user/liamnichols) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to let an agent query iCloud Find My through the PyiCloud CLI, then summarize device location, battery level, and charging status for the user's own devices or consented Family Sharing devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive iCloud Find My location, session, device, and Family Sharing data to an agent. <br>
Mitigation: Install only for accounts and devices where agent access is intended, obtain consent from affected people, and avoid storing Apple IDs in shared workspace files. <br>
Risk: The artifact includes eval()-based parsing examples for CLI location output. <br>
Mitigation: Replace eval()-based parsing with structured output, strict regex extraction, or literal parsing with validation before operational use. <br>
Risk: Proactive or repeated location checks can become unintended tracking. <br>
Mitigation: Limit proactive checks to explicit user-approved workflows and make repeated monitoring behavior visible to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liamnichols/icloud-findmy) <br>
- [PyiCloud project](https://github.com/picklepete/pyicloud) <br>
- [Required CLI: icloud](artifact/SKILL.md) <br>
- [Install PyiCloud (pipx)](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and parsed CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive iCloud Find My location, timestamp, device, and battery information.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
