## Description: <br>
Real Chrome automation for AI agents, including authenticated sessions, PII anonymization, sealed secrets, site adapters, session checkpoints, and video recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enreign](https://clawhub.ai/user/enreign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power users, and automation engineers use this skill to drive real Chrome sessions from MCP-compatible agents for authenticated web workflows, frontend verification, sensitive-data automation, and persistent browser tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can control real logged-in Chrome sessions and may access authenticated pages, persistent browser state, recordings, or sensitive account data. <br>
Mitigation: Use dedicated low-privilege Chrome profiles, enable domain allowlists, treat snapshots and recordings like credentials, and require human confirmation before external posts, form submissions, account changes, or sealed-secret command execution. <br>
Risk: Sensitive data may be exposed through page content, browser state, snapshots, recordings, or automation outputs if security controls are not configured for the workflow. <br>
Mitigation: Enable anonymization for sensitive work, avoid storing long-lived credentials in general KV state, and follow the skill's guidance for sealed secrets and audit handling. <br>
Risk: Stealth mode and unattended automation can increase misuse or policy risk when used on third-party services. <br>
Mitigation: Use stealth mode only with explicit approval and keep humans in the loop for workflows that affect external systems or accounts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/enreign/pagerunner-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/enreign) <br>
- [Repository URL from Skill Metadata](https://github.com/Enreign/pagerunner-skill) <br>
- [Quick Start Guide](SKILL.md) <br>
- [Security and Privacy](SECURITY.md) <br>
- [Complete Tool Reference](REFERENCE.md) <br>
- [Workflow Patterns](PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, shell, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps, MCP tool-call patterns, security guidance, and local setup commands.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
