## Description: <br>
Run a comprehensive local security scan on your OpenClaw installation, covering configuration, network exposure, credentials, OS hardening, and agent guardrails while keeping data local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jkahn-tr](https://clawhub.ai/user/Jkahn-tr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to assess local OpenClaw installations, review severity-scored findings, and optionally apply prompted hardening fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-fix mode can modify local OpenClaw-related files after user confirmation. <br>
Mitigation: Run the default read-only scan first, then use --fix only after reviewing each displayed command. <br>
Risk: Saved reports can reveal local paths and security findings about the user's OpenClaw setup. <br>
Mitigation: Review --report output before sharing it outside the local environment. <br>


## Reference(s): <br>
- [OpenClaw Security Scanner ClawHub release](https://clawhub.ai/Jkahn-tr/openclaw-security-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON findings and optional local report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; default mode is read-only; --fix prompts before changes; --report writes a local report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
