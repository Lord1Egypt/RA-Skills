## Description: <br>
Execute PowerShell commands reliably on Windows. Avoid &&, handle parameter parsing, recover from interruptions, and ensure cross-session continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to turn Bash-style command habits into reliable Windows PowerShell execution patterns, including safe chaining, parameter handling, path management, encoding, retries, and checkpointing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerShell examples involving web requests, deletion targets, background jobs, or checkpoint files could affect local systems if copied without review. <br>
Mitigation: Review Invoke-WebRequest destinations, Remove-Item targets, background job behavior, and checkpoint contents before running adapted commands. <br>
Risk: Logs or checkpoint files may accidentally include secrets, tokens, credentials, or request headers. <br>
Mitigation: Keep secrets out of logs and checkpoints, use environment variables or SecureString for credentials, and scan scripts for sensitive values before use. <br>


## Reference(s): <br>
- [Privacy Security Checklist](references/privacy-checklist.md) <br>
- [Microsoft PowerShell Documentation](https://docs.microsoft.com/powershell) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks, checklists, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; users should review and adapt generated PowerShell before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
