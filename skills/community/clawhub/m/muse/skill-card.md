## Description: <br>
Give ClawBot access to your team's entire coding history. Muse connects your past sessions, team knowledge, and project context, so ClawBot can help design features, mediate team discussions, and work autonomously across your codebase. Deploy at tribeclaw.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexander-morris](https://clawhub.ai/user/alexander-morris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use Muse to query past coding sessions, manage team knowledge, inspect project history, and coordinate agent workflows through the tribe CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Muse requests broad access to coding history, telemetry, knowledge-base sync, imports, and autonomous-agent features. <br>
Mitigation: Install it only when that level of access is intended, review the provider's privacy and retention terms, and avoid syncing secrets, regulated data, or proprietary code unless approved. <br>
Risk: Search, sync, import, and force-sync commands can expose more session history or project context than intended. <br>
Mitigation: Scope commands to specific projects or time ranges where possible, check telemetry status before use, and disable telemetry when collection is not intended. <br>
Risk: MUSE and CIRCUIT beta commands can spawn or manage autonomous agents that act across a codebase. <br>
Mitigation: Review agent goals and outputs before applying changes, monitor active sessions, and stop agents that are mis-scoped or no longer needed. <br>


## Reference(s): <br>
- [Muse on ClawHub](https://clawhub.ai/alexander-morris/muse) <br>
- [TribeClaw](https://tribeclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tribe CLI commands and JSON-oriented examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the tribe CLI, authentication with tribe login, and beta mode for MUSE and CIRCUIT commands.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
