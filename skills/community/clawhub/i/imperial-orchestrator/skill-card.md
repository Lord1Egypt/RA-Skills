## Description: <br>
High-availability multi-role model router for OpenClaw that discovers available models, maps them to role-based departments, routes tasks by complexity and domain, avoids dead auth chains, and degrades gracefully when providers fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexnode](https://clawhub.ai/user/rexnode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route OpenClaw work across specialized model roles for coding, operations, security, writing, legal, finance, planning, and review while preserving fallback behavior when providers fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenClaw model configuration and use configured API credentials during model validation, benchmarking, and execution. <br>
Mitigation: Install only in controlled environments, keep secrets out of prompts, and review provider configuration before running validation, benchmark, or execution commands. <br>
Risk: Prompts and benchmark tasks may be sent to configured model providers, including optional secondary review calls. <br>
Mitigation: Avoid secrets or regulated data in prompts and use the documented no-review option when secondary review calls are not desired. <br>
Risk: Routing, audit, benchmark, and session files may be stored locally. <br>
Mitigation: Set STATE_FILE, AUDIT_FILE, BENCHMARK_FILE, and SESSION_DIR to controlled locations when retention, access control, or cleanup matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rexnode/imperial-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/rexnode) <br>
- [Architecture reference](references/ARCHITECTURE.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Three Departments and Six Ministries reference](https://github.com/cft0808/edict) <br>
- [PUA prompt engineering reference](https://github.com/tanweai/pua) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON routing decisions, Markdown guidance, shell commands, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model, fallback chain, survival model, role prompts, review roles, forbidden actions, reasoning, local state files, audit files, benchmark files, and session artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
