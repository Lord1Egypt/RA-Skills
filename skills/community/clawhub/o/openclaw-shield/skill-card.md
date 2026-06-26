## Description: <br>
Enterprise AI security scanner using static analysis, runtime guards, and ClamAV to detect credential theft, data leaks, malware, and audit logging gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfaria32](https://clawhub.ai/user/pfaria32) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to scan AI agent code for suspicious patterns, review JSON security reports, and configure runtime guardrails or scheduled scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package asks users to fetch and run unpinned external code that was not included in the package. <br>
Mitigation: Review the external repository before running it, pin a specific commit, and restrict scan targets to intended directories. <br>
Risk: Cron jobs or Telegram alerts can log or transmit scan details unexpectedly if enabled without review. <br>
Mitigation: Enable scheduled scans and Telegram alerts only after confirming exactly what data is logged or transmitted. <br>


## Reference(s): <br>
- [OpenClaw Shield ClawHub page](https://clawhub.ai/pfaria32/openclaw-shield) <br>
- [Publisher profile](https://clawhub.ai/user/pfaria32) <br>
- [README](artifact/README.md) <br>
- [Security notice](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON report paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run scans, configure allowlists, enable cron jobs, or inspect generated security reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
