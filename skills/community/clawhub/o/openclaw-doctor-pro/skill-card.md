## Description: <br>
Comprehensive diagnostic, error-fixing, and skill recommendation tool for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhenixStar](https://clawhub.ai/user/PhenixStar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw issues, run health checks, apply guided or automated fixes, and identify relevant ClawHub skills for their gateway setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter an OpenClaw host through auto-fix actions, including configuration edits, file operations, package installation, service restarts, and process termination. <br>
Mitigation: Start with check-only or dry-run modes, review each proposed fix before execution, avoid broad auto-fix commands on production systems, and back up ~/.openclaw before applying changes. <br>
Risk: Diagnostic logs and configuration details may contain API keys, tokens, or other sensitive operational information. <br>
Mitigation: Do not paste API keys or full diagnostic output into chats or tickets, and redact credentials before sharing reports. <br>
Risk: The authoritative security verdict is suspicious because the troubleshooting behavior is broad and warnings are incomplete. <br>
Mitigation: Install only if this level of host-modifying troubleshooting is acceptable, keep auto-fix use scoped to known issues, and manually review changes after execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PhenixStar/openclaw-doctor-pro) <br>
- [OpenClaw Doctor Pro homepage](https://github.com/PhenixStar/openclaw-doctor-pro) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Error Catalog](references/error-catalog.md) <br>
- [Auto-Fix Capabilities](references/auto-fix-capabilities.md) <br>
- [Diagnostic Commands](references/diagnostic-commands.md) <br>
- [Troubleshooting Workflow](references/troubleshooting-workflow.md) <br>
- [ClawHub Integration](references/clawhub-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, rich terminal text, JSON, and shell commands depending on the selected tool and flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic reports, recommended fix steps, generated configuration changes, dry-run output, and ClawHub skill recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
