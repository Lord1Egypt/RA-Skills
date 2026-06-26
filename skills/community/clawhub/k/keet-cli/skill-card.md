## Description: <br>
Safely operate and improve the Keet CLI project and Keet ↔ OpenClaw bridge for read-only inspection, debugging, documentation, release checks, bridge supervision, and explicitly approved messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[projectreturn](https://clawhub.ai/user/projectreturn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, debug, document, release-check, and supervise Keet CLI and Keet to OpenClaw bridge workflows. It is intended to keep live messaging actions gated by explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound messages, file shares, invite actions, chat creation, bridge or daemon processes, and Git pushes can change external state or expose private information. <br>
Mitigation: Require explicit user confirmation of the exact profile path, target chat, message or file, process lifetime, repository, branch, and diff before those actions. <br>
Risk: Keet profile storage, private messages, invite codes, recovery material, bridge state, and logs may contain sensitive data. <br>
Mitigation: Keep this data private, avoid printing message contents unless specifically requested, and redact secrets and private messages in summaries and errors. <br>
Risk: Concurrent Keet Desktop and CLI access can conflict with profile storage locks. <br>
Mitigation: Use one explicitly approved long-running daemon owner when repeated access is needed, and route commands through the daemon socket instead of spawning competing sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/projectreturn/keet-cli) <br>
- [Project Source Listed by Skill](https://github.com/projectreturn/Keet-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include explicit confirmation prompts before state-changing messaging, file sharing, bridge, daemon, invite, chat creation, or Git push actions.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
