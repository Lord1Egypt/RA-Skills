## Description: <br>
Jarvis Core configures an agent with a proactive assistant persona, memory-loading routines, confidence calibration, emotional-response rules, and heartbeat-style follow-up behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent a persistent, proactive assistant style with cross-session memory recall, confidence signaling, emotional response modes, and follow-up behavior. It is best suited to personal-agent workflows where the user intentionally wants the assistant to reuse prior context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags broad automatic access to sensitive memories and prior context. <br>
Mitigation: Install only when the user explicitly wants persistent memory reuse; keep it off shared machines and sensitive multi-person data unless clear opt-in, deletion, scoping, and audit controls are added. <br>
Risk: The security review flags proactive monitoring behavior without enough user control. <br>
Mitigation: Require user-configurable boundaries for heartbeat checks and proactive follow-up, and require confirmation before external, irreversible, or sensitive actions. <br>
Risk: The artifact encourages emotionally framed advice and long-term persona consistency that may affect user trust and decision-making. <br>
Mitigation: Keep critical recommendations subject to human review, preserve confidence disclosures, and avoid using the skill for high-stakes personal, medical, legal, or financial decisions without independent verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/jarvis-core) <br>
- [Project homepage from Clawdis metadata](https://github.com/davidme6/jarvis-core) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and behavioral guidance for an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable tool output; the skill primarily changes assistant behavior and memory-use posture.] <br>

## Skill Version(s): <br>
3.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
