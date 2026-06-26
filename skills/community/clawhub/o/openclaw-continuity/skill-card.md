## Description: <br>
Structured continuity and follow-up skill for OpenClaw agents that routes natural dialogue between casual chat, staged memory, and tracked follow-up with carryover, closure, cooldown, quiet-hours behavior, traceability, and frontstage safety guards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redwakame](https://clawhub.ai/user/redwakame) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to add structured continuity, staged memory, tracked follow-up, and /new carryover to an existing OpenClaw agent without replacing the agent persona or bundling a chat-platform adapter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists sensitive continuity and personal context. <br>
Mitigation: Review where OPENCLAW_STATE_DIR points, keep live state out of public artifacts, and publish only sanitized examples. <br>
Risk: Follow-up or heartbeat behavior can become too proactive without clear consent and scoping. <br>
Mitigation: Disable or tightly gate proactive and heartbeat behavior, and require confirmation for health, emotional tracking, and settings changes. <br>
Risk: Optional embedding or helper scripts can expose data if connected to untrusted providers, plugin roots, or inputs. <br>
Mitigation: Use optional embedding only with trusted providers and plugin roots, and do not expose file-output or harness helpers to untrusted inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/redwakame/openclaw-continuity) <br>
- [Project Homepage](https://github.com/redwakame/openclaw-continuity) <br>
- [Install Guide](docs/install.md) <br>
- [Harness](docs/harness.md) <br>
- [Host Boundary](docs/host-boundary.md) <br>
- [V2 Known Limits](docs/v2-known-limits.md) <br>
- [Modules Reference](references/modules.md) <br>
- [Templates Reference](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON/configuration examples, and generated continuity state for agent use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus OPENCLAW_STATE_DIR and OPENCLAW_CONFIG_PATH; supported OS targets are darwin and linux.] <br>

## Skill Version(s): <br>
2.0.21 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
