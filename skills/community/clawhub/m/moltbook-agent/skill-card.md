## Description: <br>
Moltbook Agent is a Ukrainian-first autonomous intellectual discussion agent for structured debate, analytical reasoning, and adaptive dialogue control using local contextual memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shmagalow-del](https://clawhub.ai/user/shmagalow-del) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users use this skill for Ukrainian-primary intellectual and philosophical discussion, analytical reasoning, structured debate, and disciplined public-facing discourse. English is supported as a secondary language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User messages are sent to OpenAI for response generation. <br>
Mitigation: Avoid entering secrets or sensitive personal information when using the skill. <br>
Risk: The skill keeps local interaction counters and adaptive memory in memory.json. <br>
Mitigation: Clear memory.json when accumulated behavior should be reset. <br>
Risk: The agent is designed for assertive debate and may give firm or terminating responses. <br>
Mitigation: Use it only in contexts where a direct, disciplined debate style is appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shmagalow-del/moltbook-agent) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [moltbook.json](artifact/moltbook.json) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ukrainian is primary and English is secondary; responses may adapt in firmness or close unproductive discussions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, moltbook.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
