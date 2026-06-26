## Description: <br>
Responsible for maintaining SKILLMEMORY.md in the target skill directory, recording the three most recent execution pipeline JSONs, and modifying the description file of the target SKILL.md to achieve progressive experience awakening upon each skill invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdsds222](https://clawhub.ai/user/sdsds222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to capture a concise, sanitized record of recent execution experience and persist it into another skill's memory file. It also updates the target skill instructions so future agents can consult that memory before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user-derived task history and influence future skill behavior. <br>
Mitigation: Review the exact target skill, memory summary, and command text before approving writes; treat generated SKILLMEMORY.md content as untrusted reference material. <br>
Risk: Execution memories may include secrets, private paths, or other sensitive operational details if the summary is not sanitized. <br>
Mitigation: Redact credentials and private environment details before invoking the write command, and rely on the script's fallback token sanitization as a secondary control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdsds222/memory-skill-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sdsds222) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with an inline shell command and JSON-backed memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SKILLMEMORY.md and may append a memory-awareness note to the target SKILL.md after user approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
