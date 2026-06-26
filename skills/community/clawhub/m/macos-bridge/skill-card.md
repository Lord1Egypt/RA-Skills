## Description: <br>
Bridge Mac-owned tools like imsg, remindctl, memo, things, and peekaboo onto a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN, enabled-channel auto-discovery, and OpenClaw config fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose Mac-owned tools as stable Linux-side commands on a trusted same-LAN OpenClaw gateway. It helps keep wrapper-backed public skills truthful about macOS permissions, remote ownership, and Wake-on-LAN assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH wrappers delegate tool access to the configured Mac account. <br>
Mitigation: Install only for Macs you control on a trusted local network, prefer a restricted SSH key or account, and review the rendered tool-to-host map before deployment. <br>
Risk: Future agents that can run the installed wrappers may act through the configured Mac-owned tools. <br>
Mitigation: Use explicit mappings for sensitive tools, pin known_hosts where possible, and keep only required macOS-backed channels enabled. <br>


## Reference(s): <br>
- [Skill Readiness](references/skill-readiness.md) <br>
- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/macos-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wrapper paths, tool-to-host maps, SSH options, OpenClaw config references, and verification commands.] <br>

## Skill Version(s): <br>
0.6.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
