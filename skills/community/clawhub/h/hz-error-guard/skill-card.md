## Description: <br>
Monitors, classifies, and intercepts agent errors in real time, with retry, circuit-breaking, status, flush, recovery, heartbeat, and watchdog helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor long-running agent work, classify failures, emit progress and heartbeat events, and trigger controlled recovery when tasks stall or fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery commands can interrupt active agent sessions, including sessions outside the skill's own work. <br>
Mitigation: Require explicit authorization before flush or recover actions and restrict process killing to sessions spawned by this skill. <br>
Risk: Saved error context or event metadata may contain sensitive operational information. <br>
Mitigation: Define redaction rules before persisting or sharing error context, event metadata, or recovery summaries. <br>


## Reference(s): <br>
- [Huizai Error Guard ClawHub release](https://clawhub.ai/lidekahdjdhdhsjjs-lang/hz-error-guard) <br>
- [lidekahdjdhdhsjjs-lang ClawHub publisher profile](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON status and event payloads plus TypeScript helper modules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn isolated agent sessions, emit task lifecycle events, and return status, flush, recovery, heartbeat, or watchdog action summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
