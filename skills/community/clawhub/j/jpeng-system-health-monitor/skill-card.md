## Description: <br>
Monitor system health including disk space, memory usage, process status, and evolution metrics to detect potential issues early. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for local heartbeat checks, pre-change health verification, diagnostics, and alerting around disk space, memory pressure, process status, evolution cycles, and installed skill counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated health reports can expose local system and workspace details such as disk usage, memory usage, platform, uptime, Node version, evolution-cycle status, and installed-skill counts. <br>
Mitigation: Review and redact health reports before sharing them outside the intended operational context. <br>
Risk: The skill reads local diagnostic files and directories from the current workspace, so missing or stale local state can make evolution and skill-count checks incomplete. <br>
Mitigation: Run it from the intended workspace and treat warning or missing-check results as prompts for follow-up inspection rather than definitive root-cause analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-system-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [JSON-compatible JavaScript object or human-readable text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes health status, individual checks, issues, and a timestamp; reports may include local system and workspace details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
