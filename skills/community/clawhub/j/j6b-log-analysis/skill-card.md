## Description: <br>
J6B泊车系统日志读取和分析，支持日志定位、读取、常见错误识别、日志下载和系统资源性能分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderchendq](https://clawhub.ai/user/coderchendq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, test engineers, and system engineers use this skill to locate, inspect, download, and analyze J6B parking-system logs, diagnose common failures, and prepare system-resource performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root-level device access, admin commands, and live-system operations may disrupt J6B/QNX systems if used outside approved procedures. <br>
Mitigation: Limit installation and use to authorized J6B/QNX developers, testers, or operators, and require explicit operational approval before root access, process-kill, permission-change, time-setting, or background monitoring commands. <br>
Risk: Logs and coredumps can contain sensitive diagnostic, vehicle, or operational data. <br>
Mitigation: Treat logs and coredumps as sensitive, export only necessary files, and store them only in approved locations. <br>
Risk: Background monitoring and log-transfer workflows can affect live systems or consume storage when left running. <br>
Mitigation: Run monitoring during approved diagnostic windows, review generated files, and stop or clean up monitoring outputs according to operational procedure. <br>


## Reference(s): <br>
- [User Manual](用户使用手册.md) <br>
- [Log Locations](references/log-locations.md) <br>
- [Error Codes](references/error-codes.md) <br>
- [QNX Performance Analysis](references/performance.md) <br>
- [QNX Command Reference](references/qnx-commands.md) <br>
- [System Resource Report Template](references/report-template-system-resource.md) <br>
- [Troubleshooting Case Library](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured diagnostic report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference QNX diagnostic commands and local shell scripts for log download, log analysis, and CPU monitoring.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
