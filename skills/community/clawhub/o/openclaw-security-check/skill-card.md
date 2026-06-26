## Description: <br>
Security self-check for OpenClaw deployments that audits openclaw.json configuration and host security, then outputs a 10-item PASS/WARN/FAIL report with optional fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a fast security audit of an OpenClaw deployment, including gateway exposure, authentication, token strength, channel policies, config permissions, plaintext secrets, firewall state, SSH hardening, and exposed ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the bundled script has an unsafe config-parsing bug. <br>
Mitigation: Review or fix the parser before installing, and verify findings against the OpenClaw configuration before acting on remediation advice. <br>
Risk: The default audit can request elevated host inspection. <br>
Mitigation: Run the script manually only when intending to audit the deployment, review any sudo prompts, and avoid heartbeat or cron use until the sudo behavior is tightened. <br>
Risk: Firewall, SSH, and token changes can disrupt access or paired clients if applied incorrectly. <br>
Mitigation: Require user confirmation, back up configuration first, verify remote access in a second session, allow SSH before enabling firewall rules, and rerun the check after changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guoqunabc/openclaw-security-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Human-readable PASS/WARN/FAIL report, optional JSON report, and Markdown guidance with shell commands for confirmed fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit by default; optional remediation guidance requires user confirmation before changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
