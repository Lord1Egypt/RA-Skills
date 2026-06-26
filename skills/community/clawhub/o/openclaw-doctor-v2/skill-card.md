## Description: <br>
Checks OpenClaw system health across configuration, models, cron jobs, memory files, and installed skills, then reports status and repair suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l6366616-lang](https://clawhub.ai/user/l6366616-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to inspect an OpenClaw installation, summarize health, and recommend fixes. It is intended for explicit OpenClaw diagnostics and should not change configuration unless the user separately authorizes repairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostic workflow may expose local OpenClaw configuration, API-key status, cron status, installed skills, and memory or workspace file status. <br>
Mitigation: Invoke it only for intended OpenClaw diagnostics, keep reports private when they contain environment details, and redact secrets before sharing output. <br>
Risk: Repair suggestions could be applied incorrectly if treated as automatic changes. <br>
Mitigation: Treat repairs as recommendations and require explicit user approval before making any configuration or environment changes. <br>
Risk: The checks depend on a local OpenClaw environment and Node.js, so results can be incomplete when those dependencies are missing or unavailable. <br>
Mitigation: Run the skill in the intended OpenClaw workspace with Node.js and OpenClaw Gateway available, and report missing prerequisites clearly. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/l6366616-lang/openclaw-doctor-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic report with status indicators, a health score, and repair suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redacts sensitive values such as API keys and avoids configuration changes unless the user explicitly authorizes them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
