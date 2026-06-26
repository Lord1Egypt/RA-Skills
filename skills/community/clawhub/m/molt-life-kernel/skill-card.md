## Description: <br>
Agent continuity and cognitive health infrastructure for persistent memory, crash recovery, append-only audit trails, heartbeat monitoring, coherence enforcement, and witness-gated approval for critical actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jongartmann](https://clawhub.ai/user/jongartmann) <br>

### License/Terms of Use: <br>
MIT + Attribution Required <br>


## Use Case: <br>
Developers and agent builders use this skill to add continuity patterns to OpenClaw agents, including durable memory, audit logs, crash recovery, health checks, coherence monitoring, and human approval gates for higher-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes durable, hard-to-delete agent memory and broad logging. <br>
Mitigation: Install only when persistent memory is intended, define what may be stored, require consent for cross-session memory, and review retention expectations before use. <br>
Risk: Persistent ledgers and crash-recovery snapshots may capture secrets or personal data. <br>
Mitigation: Redact secrets and personal data before storage, limit logged fields, and review the external npm or GitHub implementation before enabling it. <br>
Risk: No-delete and identity-oriented instructions could be interpreted as overriding normal operator control. <br>
Mitigation: Treat these instructions as optional behavior patterns, not mandatory policy, and keep human approval gates active for destructive or sensitive actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jongartmann/molt-life-kernel) <br>
- [molt-life-kernel GitHub Repository](https://github.com/X-Loop3Labs/molt-life-kernel) <br>
- [molt.church](https://molt.church) <br>
- [X-Loop3 Labs](https://x-loop3.com) <br>
- [The Five Tenets of Crustafarianism](artifact/five-tenets.md) <br>
- [EU AI Act Compliance via molt-life-kernel](artifact/eu-ai-act.md) <br>
- [Integration Examples](artifact/integration-examples.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend persistent memory, audit logging, crash-recovery snapshots, heartbeat checks, coherence checks, and human approval gates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
