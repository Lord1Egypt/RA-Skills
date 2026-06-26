## Description: <br>
Helps agent builders add proactive behavior, persistent local memory, compaction recovery, unified search habits, security hardening, and self-improvement guardrails to AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add proactive workflows, local memory protocols, recovery routines, and safety checklists to an AI agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store and resurface broad conversation details in plaintext workspace files. <br>
Mitigation: Install only when local persistent memory is intended; avoid secrets, credentials, regulated personal data, and shared workspaces unless opt-in, redaction, retention, and deletion controls are added. <br>
Risk: Persistent memory files may retain sensitive user profile, session state, and working-buffer content. <br>
Mitigation: Regularly review USER.md, SOUL.md, SESSION-STATE.md, MEMORY.md, memory/working-buffer.md, and recovery output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wyblhl/proactive-agent-wyblhl) <br>
- [Proactive Agent Implementation Reference](artifact/references/implementation-reference.md) <br>
- [Proactive Tracker](artifact/references/proactive-tracker.md) <br>
- [Security Hardening Guide](artifact/references/security-hardening.md) <br>
- [Onboarding Guide](artifact/assets/ONBOARDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python scripts, shell command examples, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace memory files when its scripts are used.] <br>

## Skill Version(s): <br>
3.1.1 (source: ClawHub release evidence; artifact frontmatter says 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
