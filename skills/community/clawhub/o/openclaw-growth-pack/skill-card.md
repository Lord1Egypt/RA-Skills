## Description: <br>
Bootstraps a fresh OpenClaw install with model routing, gateway token consistency, anti-stall execution rules, a lightweight autonomy loop, and verification gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to turn a new OpenClaw instance into a more reliable task-completing setup. It guides model routing, token alignment, anti-stall contracts, periodic self-check routines, verification, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change core OpenClaw behavior, including model routing, gateway tokens, provider overrides, execution contracts, memory files, and scheduled checks. <br>
Mitigation: Review every proposed file change before applying it, create backups first, and keep a rollback list for AGENTS.md, HEARTBEAT.md, memory files, provider overrides, and scheduled jobs. <br>
Risk: Token values may appear in local audit output while checking gateway token consistency. <br>
Mitigation: Redact token values before sharing logs, screenshots, or audit output. <br>
Risk: Persistent anti-stall or autonomy routines can continue running outside the immediate setup task. <br>
Mitigation: Install only intentionally scoped daily or weekly checks, document each created job, and remove jobs that are not needed after validation. <br>


## Reference(s): <br>
- [OpenClaw Growth Pack Examples](references/examples.md) <br>
- [OpenClaw Growth Pack ClawHub Page](https://clawhub.ai/Dalomeve/openclaw-growth-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local configuration edits, verification gates, rollback steps, and periodic self-check routines.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
