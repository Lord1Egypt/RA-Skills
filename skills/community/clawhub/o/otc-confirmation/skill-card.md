## Description: <br>
Otc Confirmation adds an email-delivered one-time confirmation code gate for sensitive agent operations before execution proceeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lewis-404](https://clawhub.ai/user/Lewis-404) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to require human confirmation before agents perform dangerous, irreversible, externally visible, or security-sensitive operations. It provides shell scripts, prompt integration guidance, and reference security architecture materials for adding an out-of-band approval step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan states that the zero-knowledge guarantee is overstated when approval codes are pasted into chat. <br>
Mitigation: Treat the chat session as sensitive, avoid displaying or logging codes, and prefer an isolated verification path for high-impact workflows. <br>
Risk: Stale confirmation state can remain valid because the shell workflow does not provide time-based expiry. <br>
Mitigation: Clear stale state files before sensitive operations or add an expiry wrapper before relying on the confirmation gate. <br>
Risk: Custom email backends can execute a user-provided script. <br>
Mitigation: Use the default SMTP backend where practical; if a custom backend is required, allow only trusted scripts with restricted permissions. <br>
Risk: The confirmation step alone does not bind approval to a full operation policy for truly dangerous actions. <br>
Mitigation: Pair the skill with a separate operation-bound permission or risk policy wrapper before allowing destructive or high-impact operations. <br>
Risk: SMTP credentials are required for normal operation. <br>
Mitigation: Use a dedicated SMTP app password and avoid sharing the account password with the agent runtime. <br>


## Reference(s): <br>
- [Otc Confirmation ClawHub Page](https://clawhub.ai/Lewis-404/otc-confirmation) <br>
- [OTC Enforcement Checklist](references/enforcement-checklist.md) <br>
- [OTC Enforcement Discipline](references/enforcement-discipline.md) <br>
- [OTC Trigger Categories](references/trigger-categories.md) <br>
- [AI DevOps Agent Security Pack Overview](ai-devops-agent-security-pack/00_overview.md) <br>
- [Confirmation System Deep Dive](ai-devops-agent-security-pack/02_confirmation_system.md) <br>
- [OpenClaw Integration Configuration](ai-devops-agent-security-pack/examples/openclaw_config.yaml) <br>
- [Gmail App Password Help](https://support.google.com/accounts/answer/185833) <br>
- [himalaya CLI](https://github.com/pimalaya/himalaya) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Code, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands, JSON/YAML configuration snippets, and reference code files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the default SMTP path and OTC_EMAIL_RECIPIENT, OTC_SMTP_USER, and OTC_SMTP_PASS environment variables for email delivery.] <br>

## Skill Version(s): <br>
3.1.0 (source: changelog and server release, released 2026-03-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
